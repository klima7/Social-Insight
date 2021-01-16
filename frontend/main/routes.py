import os.path
import tempfile
from threading import Thread

from flask import *
from flask_babel import _, get_locale
from flask_login import login_required, current_user

import analytics
from config import config
from db import *
from frontend.common import display_errors_with_flash
from frontend.mail import send_email
from frontend.render import render_pdf
from . import main
from .forms import RenamePackForm, RenameCollationForm, ContactForm
import frontend.render as render


@main.route('/favicon.ico')
def favicon():
    return send_from_directory('static', 'favicon.ico', mimetype='image/vnd.microsoft.icon')


@main.route('/')
def index():
    return render_template('index.html')


@main.route('/', methods=['POST'])
def index_post():
    pack = Pack(status=Pack.STATUS_PENDING, name=_('Pack'))

    if current_user.is_authenticated:
        pack.user = current_user

    db_session.add(pack)
    db_session.commit()

    session['packid'] = pack.id
    session.modified = True

    uploaded_file = request.files['file']
    path = os.path.join(tempfile.mkdtemp(), 'something')
    uploaded_file.save(path)

    thread = Thread(target=analytics.analyse, args=[pack.id, path])
    thread.start()

    return jsonify({'id': pack.id})


@main.route('/example/')
def example():
    pack = db_session.query(Pack).filter_by(example=True).first()
    if pack is None:
        flash(_('Sorry, example pack is not available'), 'warning')
        return redirect(url_for('main.index'))
    return redirect(url_for('main.graphs_category', id=pack.id, category='messages'))


@main.route('/lang/<lang>')
def change_language(lang):
    if lang not in config.LANGUAGES:
        return abort(404)
    session['lang'] = lang
    return redirect(session.get('prev_url', url_for('main.index')))


@main.route('/account/')
@login_required
def account():
    return render_template('account.html')


def get_pack(id):
    pack = db_session.query(Pack).filter_by(id=id).first()
    if current_user.is_authenticated and pack.userid == current_user.id or \
            pack.id == session.get('packid', None) or pack.example:
        return pack
    abort(403)


@main.route('/packs/<id>/remove/confirm')
def remove_pack_confirm(id):
    get_pack(id)
    address = url_for('main.remove_pack', id=id)
    flash(_('Are you sure that you want to remove this pack?')+f' <a href="{address}">'+_('Yes')+'</a>', 'warning')
    return redirect(session.get('prev_url', url_for('main.account')))


@main.route('/packs/<id>/remove')
def remove_pack(id):
    pack = get_pack(id)
    db_session.delete(pack)
    db_session.commit()
    flash(_('Pack was removed'), 'success')
    return redirect(url_for('main.account'))


@main.route('/collations/create')
@login_required
def create_collation():
    collation = Collation(name=_('Collation'))
    collation.user = current_user
    db_session.add(collation)
    db_session.commit()
    flash(_('New collation was created'), 'success')
    return redirect(url_for('main.account'))


def get_collation(id):
    collation = db_session.query(Collation).filter_by(userid=current_user.id, id=id).first()
    if collation is None:
        abort(403)
    return collation


@main.route('/collations/<id>', methods=['GET', 'POST'])
@login_required
def collation(id):
    collation = get_collation(id)
    form = RenameCollationForm()
    if form.validate_on_submit():
        collation.name = form.name.data
        flash(_('Collation name changed to %(name)s', name=collation.name), 'success')
        db_session.add(collation)
        db_session.commit()
    return render_template('collation.html', collation=collation, form=form)


@main.route('/collations/<id>/remove/confirm')
def remove_collation_confirm(id):
    get_collation(id)
    address = url_for('main.remove_collation', id=id)
    flash(_('Are you sure that you want to remove this collation?')+f' <a href="{address}">'+_('Yes')+'</a>', 'warning')
    return redirect(url_for('main.collation', id=id))


@main.route('/collations/<id>/remove')
def remove_collation(id):
    collation = get_collation(id)
    db_session.delete(collation)
    db_session.commit()
    flash(_('collation was removed'), 'success')
    return redirect(url_for('main.account'))


@main.route('/packs/<id>/<category>', methods=['GET', 'POST'])
def graphs_category(id, category):
    pack = get_pack(id)
    form = RenamePackForm()

    if form.validate_on_submit():
        pack.name = form.name.data
        flash(_('Pack name changed to %(name)s', name=pack.name), 'success')
        db_session.add(pack)
        db_session.commit()

    graphs = pack.graphs.filter(Graph.category == category).order_by(Graph.id).all()
    return render_template('category.html', pack=pack, graphs=graphs, form=form, category=category)


@main.route('/packs/waiting/<packid>')
def waiting(packid):
    return render_template('waiting.html', packid=packid)


@main.route('/credits')
def credits():
    return render_template('credits.html')


@main.route('/graphs/<id>')
def graphs(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph is None:
        abort(404)
    graph.public or get_pack(graph.pack.id)
    return render_template('graph.html', graph=graph)


@main.route('/contact/', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if form.validate_on_submit():
        message = Message(sender=form.email.data, topic=form.topic.data, content=form.content.data, language=str(get_locale()))
        db_session.add(message)
        db_session.commit()

        send_email(config.MAIL_USERNAME, _('Message'), 'contact', form=form)
        flash(_('Message was sent'), 'success')
        return redirect(url_for('main.contact'))

    if current_user.is_authenticated:
        form.email.data = current_user.email

    display_errors_with_flash(form)
    return render_template('contact.html', form=form)


@main.route('/mode/dark')
def dark_mode():
    session['dark_mode'] = True
    return redirect(session.get('prev_url', url_for('main.index')))


@main.route('/mode/light')
def light_mode():
    session['dark_mode'] = False
    return redirect(session.get('prev_url', url_for('main.index')))


@main.route('/authors')
def authors():
    return render_template('authors.html')


@main.route('/graphs/<id>/download/png')
def download_graph_png(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph is None:
        abort(404)

    directory = tempfile.mkdtemp()
    name = graph.get_name() + ".png"
    path = os.path.join(directory, name)
    render.render_chart_png(graph, path)
    return send_from_directory(directory=directory, filename=name, as_attachment=True)


@main.route('/graphs/<id>/download/svg')
def download_graph_svg(id):
    graph = db_session.query(Graph).filter_by(id=id).first()
    if graph is None:
        abort(404)

    directory = tempfile.mkdtemp()
    name = graph.get_name() + ".svg"
    path = os.path.join(directory, name)
    render.render_chart_svg(graph, path)
    return send_from_directory(directory=directory, filename=name, as_attachment=True)


def something2pdf(container):
    style = request.args.get('style', 'fancy')
    directory = tempfile.mkdtemp()
    name = f'{container.name}.pdf'
    path = os.path.join(directory, name)

    file = File(path=path)
    db_session.add(file)
    db_session.commit()

    session['fileid'] = file.id

    thread = Thread(target=render.render_pdf, args=[container, path, file, str(get_locale()), style])
    thread.start()


@main.route("/collations/<id>/pdf")
def collation2pdf(id):
    collation = get_collation(id)
    something2pdf(collation)
    return redirect(url_for('main.file_waiting'))


@main.route("/packs/<id>/pdf")
def pack2pdf(id):
    pack = get_pack(id)
    something2pdf(pack)
    return redirect(url_for('main.file_waiting'))


def generate_charts_zip(container, categories):
    directory = tempfile.mkdtemp()
    name = container.name + ".zip"
    path = os.path.join(directory, name)

    file = File(path=path)
    db_session.add(file)
    db_session.commit()

    session['fileid'] = file.id

    thread = Thread(target=render.render_zip, args=[container, path, file, categories])
    thread.start()


@main.route('/packs/<id>/download')
def download_pack_zip(id):
    pack = get_pack(id)
    generate_charts_zip(pack, True)
    return redirect(url_for('main.file_waiting'))


@main.route('/collations/<id>/download')
def download_collation_zip(id):
    collation = get_collation(id)
    generate_charts_zip(collation, False)
    return redirect(url_for('main.file_waiting'))


@main.route('/files/waiting')
def file_waiting():
    return render_template('waiting_file.html')


@main.route('/files/download')
def file_download():
    fileid = session.get('fileid', None)
    if fileid is None:
        abort(404)
    file = db_session.query(File).filter_by(id=fileid).first()
    if file is None or not file.ready:
        abort(404)

    directory, name = os.path.split(file.path)
    return send_from_directory(directory=directory, filename=name, as_attachment=True)




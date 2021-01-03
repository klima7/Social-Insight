import os

import click

import db
from frontend import create_app
from config import config


app = create_app()


@app.cli.command(help="Clean database and remove uploaded files.")
def clean():
    db.clean_db()
    print("Database cleaned and uploaded files removed")


@app.cli.group(help="Translation commands.")
def translate():
    pass


@translate.command(help="Initialize a new language.")
@click.argument('lang')
def init(lang):
    pot_location = os.path.join(config.BABEL_TRANSLATIONS_LOCATION, 'messages.pot')
    if os.system(f'pybabel extract -F {config.BABEL_CONFIG_LOCATION} -k _l -o {pot_location} .'):
        raise RuntimeError('extract command failed')
    if os.system(f'pybabel init -i {pot_location} -d {config.BABEL_TRANSLATIONS_LOCATION} -l ' + lang):
        raise RuntimeError('init command failed')
    os.remove(pot_location)
    print("Language init success")


@translate.command(help="Update all languages.")
def update():
    pot_location = os.path.join(config.BABEL_TRANSLATIONS_LOCATION, 'messages.pot')
    if os.system(f'pybabel extract -F {config.BABEL_CONFIG_LOCATION} -k _l -o {pot_location} .'):
        raise RuntimeError('extract command failed')
    if os.system(f'pybabel update -i {pot_location} -d {config.BABEL_TRANSLATIONS_LOCATION}'):
        raise RuntimeError('update command failed')
    os.remove(pot_location)
    print("Translations update success")


@translate.command(help="Compile all languages.")
def compile():
    if os.system(f'pybabel compile -d {config.BABEL_TRANSLATIONS_LOCATION}'):
        raise RuntimeError('compile command failed')
    print("Compilation success")


@app.cli.command(help="Update example data file.")
@click.argument('name')
def example(name):
    try:
        db.example_pack_update(name)
    except FileNotFoundError:
        print("Unable to find file " + name)
    else:
        print("Updating example pack")






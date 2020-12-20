from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from frontend.auth.forms import EMAIL_VALIDATOR


class UploadForm(FlaskForm):
    upload = FileField('file', validators=[FileRequired(), FileAllowed(['json'])])
    submit = SubmitField()


class RenamePackForm(FlaskForm):
    name = StringField(_l('New pack name'), validators=[DataRequired()])
    submit = SubmitField(_l('Rename'))


class RenameCollationForm(FlaskForm):
    name = StringField(_l('New collation name'), validators=[DataRequired()])
    submit = SubmitField(_l('Rename'))


class ContactForm(FlaskForm):
    TOPICS = [_l('Opinion about application'),
              _l('New feature proposition'),
              _l('Bug reporting'),
              _l('Other')]

    email = StringField(_l('Your email'), validators=[DataRequired(), EMAIL_VALIDATOR])
    topic = SelectField(_l('Topic'), choices=TOPICS)
    content = TextAreaField(_l('Content'), validators=[DataRequired()])
    submit = SubmitField(_l('Send'))

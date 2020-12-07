from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField, StringField, SelectField, TextAreaField
from wtforms.validators import DataRequired
from frontend.auth.forms import EMAIL_VALIDATOR


class UploadForm(FlaskForm):
    VALID_EXTENSIONS = ['json']

    upload = FileField('image', validators=[FileRequired(), FileAllowed(VALID_EXTENSIONS)])
    submit = SubmitField()


class RenamePackForm(FlaskForm):
    name = StringField('New name', validators=[DataRequired()])
    submit = SubmitField('Rename')


class RenameCollationForm(FlaskForm):
    name = StringField('New collation name', validators=[DataRequired()])
    submit = SubmitField('Rename')


class ContactForm(FlaskForm):
    email = StringField('Your email', validators=[DataRequired(), EMAIL_VALIDATOR])
    topic = SelectField('Topic', choices=['New feature proposition', 'Bug reporting', 'Other'])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Send')

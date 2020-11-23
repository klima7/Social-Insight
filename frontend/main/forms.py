from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField, StringField
from wtforms.validators import DataRequired


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

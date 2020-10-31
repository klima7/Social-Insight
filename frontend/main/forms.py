from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired, FileAllowed
from wtforms import SubmitField, FileField


class UploadForm(FlaskForm):
    VALID_EXTENSIONS = ['json']

    upload = FileField('image', validators=[FileRequired(), FileAllowed(VALID_EXTENSIONS)])
    submit = SubmitField()

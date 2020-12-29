from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import SubmitField, TextAreaField
from wtforms.validators import DataRequired


class ReplyForm(FlaskForm):
    response = TextAreaField(_l('Response'), validators=[DataRequired()])
    submit = SubmitField(_l('Reply'))

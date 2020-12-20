from db import *
from flask_wtf import FlaskForm
from flask_babel import lazy_gettext as _l
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

EMAIL_VALIDATOR = Email(message=_l('Invalid email address'))


class LoginForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), EMAIL_VALIDATOR])
    password = PasswordField(_l('Password'), validators=[DataRequired()])
    remember_me = BooleanField(_l('Keep me logged in'))
    submit = SubmitField(_l('Log In'))


class RegisterForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), EMAIL_VALIDATOR])
    password = PasswordField(_l('Password'), validators=[DataRequired(), Length(min=config.MIN_PASSWORD_LENGTH, message=_l('Password must have at least %(count)s characters', count=config.MIN_PASSWORD_LENGTH))])
    password_confirmation = PasswordField(_l('Repeat password'), validators=[DataRequired(), EqualTo('password', message=_l('Passwords must match'))])
    submit = SubmitField(_l('Register'))

    @staticmethod
    def validate_email(_, field):
        if db_session.query(User).filter_by(email=field.data.lower()).first():
            raise ValidationError(_l('Email already registered'))


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField(_l('Current password'), validators=[DataRequired()])
    new_password = PasswordField(_l('New password'), validators=[DataRequired(), Length(min=config.MIN_PASSWORD_LENGTH, message=_l('Password must have at least %(count)s characters', count=config.MIN_PASSWORD_LENGTH))])
    new_password_confirmation = PasswordField(_l('Repeat new password'), validators=[DataRequired(), EqualTo('new_password', message=_l('Passwords must match'))])
    submit = SubmitField(_l('Change'))


class ResetPasswordEmailForm(FlaskForm):
    email = StringField(_l('Email'), validators=[DataRequired(), EMAIL_VALIDATOR])
    submit = SubmitField(_l('Reset'))


class ResetPasswordForm(FlaskForm):
    password = PasswordField(_l('New password'), validators=[DataRequired(), Length(min=config.MIN_PASSWORD_LENGTH, message=_l('Password must have at least %(count)s characters', count=config.MIN_PASSWORD_LENGTH))])
    password_confirmation = PasswordField(_l('Repeat new password'), validators=[DataRequired(), EqualTo('password', message=_l('Passwords must match'))])
    submit = SubmitField(_l('Reset'))

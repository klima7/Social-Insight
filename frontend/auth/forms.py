from db import *
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length, ValidationError

EMAIL_VALIDATOR = Email(message='Invalid email address')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), EMAIL_VALIDATOR]);
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), EMAIL_VALIDATOR])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=config.MIN_PASSWORD_LENGTH, message=f'Password must have at least {config.MIN_PASSWORD_LENGTH} characters')])
    password_confirmation = PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')

    @staticmethod
    def validate_email(_, field):
        if db_session.query(User).filter_by(email=field.data.lower()).first():
            raise ValidationError('Email already registered')


class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current password', validators=[DataRequired()])
    new_password = PasswordField('New password', validators=[DataRequired(), Length(min=config.MIN_PASSWORD_LENGTH, message=f'New password must have at least {config.MIN_PASSWORD_LENGTH} characters')])
    new_password_confirmation = PasswordField('Repeat new password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')])
    submit = SubmitField('Change')

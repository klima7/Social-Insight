from config import config
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Email, Length


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

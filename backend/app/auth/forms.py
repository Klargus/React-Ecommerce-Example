# -*- coding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, EqualTo
from app.models import User
from wtforms import ValidationError
  
# Create Login Form
class LoginForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired()])
    password = PasswordField('Password:', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me:')    # Checkbox field
    submit = SubmitField('Login')


# Create Register Form
class RegisterForm(FlaskForm):
    username = StringField('Username:', validators=[DataRequired()])
    email = StringField('Email:', validators=[DataRequired(), Email(message='Invalid Email')])
    password = PasswordField('Password:', validators=[DataRequired()])
    pass_confirm = PasswordField('Confirm Password:', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already exists')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already exists')
    
    def validate_password(self, password):
        if len(password.data) < 8:
            raise ValidationError('Password must be at least 8 characters long')
        if password.data != self.pass_confirm.data:
            raise ValidationError('Passwords do not match')
        if not any(char.isdigit() for char in password.data):
            raise ValidationError('Password must contain at least one number')
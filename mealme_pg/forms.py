from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, FloatField, IntegerField, SelectMultipleField, widgets
from wtforms.validators import DataRequired, Length, Email, EqualTo

class signup_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    confirm_password = PasswordField('confirm_Password', validators=[DataRequired(), Length(min=8, max=20), EqualTo('password')])
    name = StringField('Name', validators=[DataRequired(), Length(max=20)])
    height = FloatField('Height', validators=[DataRequired()])
    weight = FloatField('Weight', validators=[DataRequired()])
    age = IntegerField('Age', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

class login_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=20)])
    submit = SubmitField('Login')
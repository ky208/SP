from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField,IntegerField,SelectField,PasswordField,validators
from wtforms.validators import Length, InputRequired, ValidationError,NumberRange,DataRequired,EqualTo

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")
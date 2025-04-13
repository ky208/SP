from flask_wtf import FlaskForm
from wtforms import FloatField, SubmitField, StringField,IntegerField,SelectField,PasswordField,validators
from wtforms.validators import Length, InputRequired, ValidationError,NumberRange,DataRequired,EqualTo

def validateYear(form,field):
    if field.data is not None and field.data<1900:
        raise ValidationError("Year should be >1900")

def validateMileage(form,field):
    if field.data is not None and field.data<0:
        raise ValidationError("Mileage cannot be negative")    
    
def validateTax(form,field):
    if field.data is not None and field.data<0:
        raise ValidationError("Tax cannot be negative")    
    
def validateMPG(form,field):
    if field.data is not None and field.data<0:
        raise ValidationError("MPG cannot be negative")
    
def validateEngineSize(form,field):
    if field.data is not None and field.data<0:
        raise ValidationError("Engine Size cannot be negative")    
    
class PredictionForm(FlaskForm):
    model = SelectField("Model",choices=['B-MAX','C-MAX','EcoSport','Edge','Escort','Fiesta','Focus','Fusion','Galaxy','Grand C-MAX','Grand Tourneo Connect','KA','Ka+','Kuga','Mondeo','Mustang','Puma','Ranger','S-MAX','Streetka','Tourneo Connect'], validators=[validators.DataRequired()])
    year = IntegerField("Year",validators=[InputRequired(),validateYear])
    transmission = SelectField("Transmission",choices=['Automatic','Manual','Semi-Auto'],validators=[InputRequired()])
    mileage = IntegerField("Mileage",validators=[InputRequired(),validateMileage])
    tax = IntegerField("Tax",validators=[InputRequired(),validateTax])
    mpg = FloatField("MPG",validators=[InputRequired(),validateMPG])
    engineSize = FloatField("Engine Size",validators=[InputRequired(),validateEngineSize])
    submit = SubmitField("Predict")

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
    username = StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password',validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password',validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField("Register")
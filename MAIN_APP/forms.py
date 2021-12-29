from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from MAIN_APP.models import User


class Register_form(FlaskForm):
    username = StringField(label='User Name', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email address', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm password', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username = username_to_check.data).first()
        if user:
            raise ValidationError('username already exists')

    def validate_email_address(self, email_to_check):
        email = User.query.filter_by(email_address = email_to_check.data).first()
        if email:
            raise ValidationError('Email already exists')



class Login_form(FlaskForm):
    username = StringField(label='Username', validators=[DataRequired()])
    password = PasswordField(label='Password', validators=[DataRequired()])
    submit = SubmitField(label='Sign in')



class AddItem(FlaskForm):
    title = StringField(label='Title', validators=[DataRequired(), Length(min=2, max=80)])
    description = TextAreaField(label='Description', validators=[DataRequired(), Length(min=2, max=500)])
    submit = SubmitField(label='Add')


class Delete_Form(FlaskForm):
    submit = SubmitField(label='Delete')

class Edit_Form(FlaskForm):
    submit = SubmitField(label='Update')
    text = TextAreaField(label='Data', validators=[DataRequired(), Length(min=2, max=500)])



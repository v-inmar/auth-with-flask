from flask import current_app
from sqlalchemy.exc import SQLAlchemyError
from flask_wtf import FlaskForm
from wtforms import validators, EmailField, PasswordField, StringField, SubmitField
from app import db
from app.models.user_model import UserModel
from app.utils.result_utils import Error, Ok, Result



class SignupForm(FlaskForm):
    firstname = StringField(label="Firstname", validators=[validators.DataRequired(), validators.Length(min=3, max=128)])
    lastname = StringField(label="Lastname", validators=[validators.DataRequired(), validators.Length(min=3, max=128)])
    email = EmailField(label="Email Address", validators=[validators.DataRequired(), validators.Length(max=255), validators.Email()])
    password = PasswordField(label="Password", validators=[validators.DataRequired(), validators.Length(min=8, max=70)])
    repeat = PasswordField(label="Repeat Password", validators=[validators.DataRequired(), validators.EqualTo("password")])
    submit = SubmitField('Submit')

    def validate_email(self, form_email):
        '''
        Check if email is already in use. This is part of the validation.
        '''
        user_result: Result[UserModel | None, SQLAlchemyError] = UserModel.get_by_email(email=str(form_email.data).strip().lower())
        if isinstance(user_result, Error):
            current_app.logger.error(user_result.error)
            raise validators.ValidationError("Server error.Try refreshing the page first.")
        
        if user_result.data is not None:
            raise validators.ValidationError("Email address already in use.")
        
        return None


class LoginForm(FlaskForm):
    email = EmailField(label="Email Address", validators=[validators.DataRequired()])
    password = PasswordField(label="Password", validators=[validators.DataRequired()])
    submit = SubmitField('Login')

    # No custom validation - I want to customize the message
    # if either are invalid, both form will get the same error message
    # i.e. Invalid email and/or password

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, SelectField
from wtforms.validators import DataRequired, Length, URL, ValidationError
from .models import *
from book_app.extensions import bcrypt

class BookForm(FlaskForm):
    title = StringField("Book Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    photo_url = StringField("Photo URL", validators=[DataRequired()])
    category = SelectField("Genre", choices=BookGenre.choices(), validators=[DataRequired()])
    submit = SubmitField("Submit")

class SignUpForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')
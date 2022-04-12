from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField, PasswordField, SubmitField, StringField
from wtforms.validators import DataRequired


class EditForm(FlaskForm):
    name = StringField('Имя', validators=[DataRequired()])
    surname = StringField('Фамилия', validators=[DataRequired()])
    nic = StringField('Ник:', validators=[DataRequired()])
    email = EmailField('Почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    password_again = PasswordField('Повторно введите пароль', validators=[DataRequired()])
    submit = SubmitField('Применить')
from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField, PasswordField, SubmitField, StringField, IntegerField, FileField 
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class SongForm(FlaskForm):
    name = StringField('Название песни:', validators=[DataRequired()])
    authors = StringField('Авторы песни через запятую:', validators=[DataRequired()])
    link = StringField('Ссылка на клип:', validators=[DataRequired()])
    year = IntegerField('Год создания:', validators=[DataRequired()])
    file = FileField('Пароль', validators=[FileRequired(), FileAllowed(["mp3"], "Некорректное",)])
    submit = SubmitField('Добавить песню')
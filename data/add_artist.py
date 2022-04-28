from flask_login import LoginManager
from flask_wtf import FlaskForm
from wtforms import EmailField, BooleanField, PasswordField, SubmitField, StringField, IntegerField, FileField 
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


class ArtistForm(FlaskForm):
    name = StringField('Имя артиста', validators=[DataRequired()])
    file = FileField('Квадратное фото артиста:', validators=[FileRequired(), FileAllowed(["jpg"], "Некорректное расширение.",)])
    submit = SubmitField('Добавить артиста')
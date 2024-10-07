from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, EmailField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm



class RegistrationForm(FlaskForm):
    login = StringField(label='Логин', validators=[DataRequired(), Length(min=5, max=50)])
    phone = StringField(label='Номер телефона', validators=[DataRequired()])
    email = EmailField(label='Электронная почта', validators=[DataRequired()])
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    avatar = FileField(label="Аватарка", validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    confirm_password = PasswordField(label='Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    password = PasswordField(label='Пароль', validators=[DataRequired()])
    login = StringField(label='Логин', validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField('Войти')

class CommentAdd(FlaskForm):
    content = TextAreaField(label='Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')


class PublicationCreate(FlaskForm):
    title = StringField(label='Заголовок', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField(label='Статья')
    hashtags = StringField(label='Хештеги')
    image = FileField(label='Фотки', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    video = FileField(label='Видео', validators=[FileAllowed(['mp4', 'mov'])])
    audio = FileField(label='Аудио', validators=[FileAllowed(['mp3', 'mov'])])
    location = StringField(label='Локация')
    mentions = StringField(label='Упоминуть пользователя')
    submit = SubmitField('Создать публикацию')



class PublicationUpdate(FlaskForm):
    title = StringField(label='Заголовок', validators=[DataRequired(), Length(max=255)])
    content = TextAreaField(label='Статья')
    hashtags = StringField(label='Хештеги')
    image = FileField(label='Фотки', validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    video = FileField(label='Видео', validators=[FileAllowed(['mp4', 'mov'])])
    audio = FileField(label='Аудио', validators=[FileAllowed(['mp3', 'mov'])])
    location = StringField(label='Локация')
    mentions = StringField(label='Упоминуть пользователя')
    submit = SubmitField('Обновить публикацию')

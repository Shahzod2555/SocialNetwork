from flask_wtf.file import FileAllowed
from wtforms.fields.simple import StringField, EmailField, PasswordField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, Length, EqualTo
from flask_wtf import FlaskForm


class RegistrationForm(FlaskForm):
    login = StringField('Логин', validators=[DataRequired(), Length(min=5, max=50)])
    phone = StringField('Номер телефона', validators=[DataRequired()])
    email = EmailField('Электронная почта', validators=[DataRequired()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    avatar = FileField("Аватарка", validators=[FileAllowed(['png', 'jpeg', 'jpg'])])
    confirm_password = PasswordField('Подтвердите пароль', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')

class LoginForm(FlaskForm):
    password = PasswordField('Пароль', validators=[DataRequired()])
    login = StringField('Логин', validators=[DataRequired(), Length(min=5, max=50)])
    submit = SubmitField('Войти')

class CommentAdd(FlaskForm):
    content = TextAreaField('Комментарий', validators=[DataRequired()])
    submit = SubmitField('Отправить')
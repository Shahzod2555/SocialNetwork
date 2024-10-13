import random

from flask import Blueprint, redirect, render_template, flash, request, url_for, session
from flask_login import current_user, login_user, logout_user
from flask_mail import Message

from ..extentions import db, bcrypt, mail
from ..forms import RegistrationForm, LoginForm, EmailForm, CodForm
from ..functions import save_ava_picture
from ..model.user import User

reg_auth = Blueprint('reg_auth_blueprint', __name__)


@reg_auth.route('/register/email', methods=['POST', 'GET'])
def email_register():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')

    email_form = EmailForm()
    if email_form.validate_on_submit():

        if User.query.filter_by(email=email_form.email.data).first():
            flash("Этот email уже зарегистрирован. Пожалуйста, используйте другой.", "danger")
            return render_template('reg_auth/register.html', email_form=email_form)

        code = random.randint(1000, 10000)
        session['verification_code'] = code
        session['email'] = email_form.email.data

        msg = Message(subject="Подтверждение почты", html=f"""
            <html>
                <head>
                    <style>
                        body {{
                            font-family: Arial, sans-serif;
                            background-color: #f4f4f4;
                            margin: 0;
                            padding: 0;
                            text-align: center;
                        }}
                        .email-container {{
                            background-color: #ffffff;
                            border-radius: 10px;
                            padding: 20px;
                            margin: 50px auto;
                            width: 80%;
                            max-width: 600px;
                            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                        }}
                        h2 {{
                            color: #007BFF;
                        }}
                        .code-container {{
                            display: inline-block;
                            padding: 15px;
                            background-color: #f0f0f0;
                            border-radius: 5px;
                            font-size: 24px;
                            color: #333;
                            cursor: text; /* Указатель мыши для выделения */
                            user-select: all; /* Позволяет выделять текст */
                        }}
                        .copy-hint {{
                            margin-top: 10px;
                            color: #777;
                            font-size: 14px;
                        }}
                        .footer {{
                            margin-top: 20px;
                            color: #555;
                            font-size: 12px;
                        }}
                    </style>
                </head>
                <body>
                    <div class="email-container">
                        <h2>Подтверждение почты</h2>
                        <p>Спасибо за регистрацию! Ваш код подтверждения:</p>
                        <div class="code-container">
                            {code}
                        </div>
                        <p class="copy-hint">Выделите и скопируйте код</p>
                        <p>Введите этот код на сайте для завершения регистрации.</p>
                        <div class="footer">
                            <p>С уважением, команда вашей социальной сети</p>
                        </div>
                    </div>
                </body>
            </html>
            """, recipients=[f"{email_form.email.data}"])
        mail.send(msg)
        return redirect(url_for('reg_auth_blueprint.cod'))

    return render_template("reg_auth/email-register.html", email_form=email_form)


@reg_auth.route('/register/cod', methods=['POST', 'GET'])
def cod():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')
    code_form = CodForm()

    if code_form.validate_on_submit():
        entered_code = code_form.cod.data
        session_code = session.get('verification_code')

        if entered_code == session_code:
            flash("Код подтвержден. Теперь вы можете продолжить регистрацию.", "success")
            return redirect(url_for('reg_auth_blueprint.register'))
        else:
            flash("Неправильный код, попробуйте еще раз.", "danger")

    return render_template("reg_auth/cod.html", code_form=code_form)


@reg_auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')

    form = RegistrationForm()
    if form.validate_on_submit():

        if User.query.filter_by(username=form.login.data).first():
            flash("Такой UserName уже занят! Выберите другой UserName.", "danger")
            return render_template('reg_auth/register.html', form=form)

        if User.query.filter_by(phone=form.phone.data).first():
            flash("С этим номером телефона уже зарегистрированы!", "danger")
            return render_template('reg_auth/register.html', form=form)

        user = User(username=form.login.data, phone=form.phone.data, email=session.get('email'),
                    password=bcrypt.generate_password_hash(form.password.data).decode('utf-8'),
                    avatar=save_ava_picture(form.avatar.data) if form.avatar.data else 'ava.svg'
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            next_page = request.args.get('next')
            flash("Регистрация прошла успешно!", "success")
            return redirect(next_page) if next_page else redirect('/')
        except Exception as e:
            print(str(e))
            flash("При регистрации произошла ошибка, попробуйте еще раз", "danger")
            return render_template('reg_auth/register.html', form=form)

    return render_template('reg_auth/register.html', form=form)


@reg_auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')

    form = LoginForm()
    if form.validate_on_submit():
        username = form.login.data
        password = form.password.data

        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password, password):
            login_user(user)
            next_page = request.args.get('next')
            flash('Успешный вход.', 'success')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Ошибка входа. Пожалуйста проверьте логин или пароль', 'danger')

    return render_template('reg_auth/login.html', form=form)


@reg_auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')

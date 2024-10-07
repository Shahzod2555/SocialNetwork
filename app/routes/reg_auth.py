from flask import Blueprint, redirect, render_template, flash, request
from flask_login import current_user, login_user, logout_user
from ..forms import RegistrationForm, LoginForm
from ..extentions import db, bcrypt
from ..functions import save_ava_picture
from ..model.user import User

reg_auth = Blueprint('reg_auth_blueprint', __name__)

@reg_auth.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        if form.avatar.data:
            avatar = save_ava_picture(form.avatar.data)
        else:
            avatar = 'ava.svg'

        user = User(
            username=form.login.data, phone=form.phone.data,
            email=form.email.data, password=hashed_password,
            avatar=avatar
        )
        try:
            db.session.add(user)
            db.session.commit()
            login_user(user)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/')
        except Exception as e:
            print(str(e))
            flash("При регистрации произошла ошибка", "error")

    return render_template('reg_auth/register.html', form=form)


@reg_auth.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        next_page = request.args.get('next')
        return redirect(next_page) if next_page else redirect('/')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            flash('Успешный вход.', 'success')
            return redirect(next_page) if next_page else redirect('/')
        else:
            flash('Ошибка входа. Пожалуйста проверьте логин или пароль', 'error')
    return render_template('reg_auth/login.html', form=form)


@reg_auth.route('/logout')
def logout():
    logout_user()
    return redirect('/')
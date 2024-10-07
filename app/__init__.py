from flask_admin.contrib.sqla import ModelView
from flask_login import login_manager
from flask_admin import Admin
from flask import Flask

from .extentions import db, migrate, login_manager
from .config import Config

from .model.publication import Publication
from .model.subscription import Subscription
from .model.comment import Comment
from .model.user import User
from .model.like import Like
from .model.viewing import Viewing

from .routes.comment import comment_blueprint
from .routes.publication import publication
from .routes.like import like_blueprint
from .routes.reg_auth import reg_auth
from .routes.message import message_view
from .routes.subscription import subscription
from .routes.main import main
from .routes.user import user
from .utils import utils_blueprint


def create_app(config_class=Config):
    app = Flask(__name__)
    admin = Admin(app, name='MyAdmin', template_mode='bootstrap4')

    app.config.from_object(config_class)

    app.register_blueprint(comment_blueprint, name='comment_blueprint')
    app.register_blueprint(publication, name='publication_blueprint')
    app.register_blueprint(subscription, name='subscription_blueprint')
    app.register_blueprint(like_blueprint, name='like_blueprint')
    app.register_blueprint(reg_auth, name='reg_auth_blueprint')
    app.register_blueprint(utils_blueprint, name='utils_blueprint')
    app.register_blueprint(message_view, name='message_blueprint')
    app.register_blueprint(main, name='main_blueprint')
    app.register_blueprint(user, name='user_blueprint')

    db.init_app(app)
    migrate.init_app(app, db)

    login_manager.init_app(app)
    login_manager.login_view = 'reg_auth_blueprint.login'
    login_manager.login_message = "Вы не можете получить доступ к данной странице."

    with app.app_context():
        db.create_all()

    admin.add_view(ModelView(Publication, db.session, name="Публикации"))
    admin.add_view(ModelView(Subscription, db.session, name="Подписчики"))
    admin.add_view(ModelView(Comment, db.session, name="Комментарии"))
    admin.add_view(ModelView(User, db.session, name="Пользователи"))
    admin.add_view(ModelView(Viewing, db.session, name="Просмотры"))
    admin.add_view(ModelView(Like, db.session, name="Лайки"))

    return app

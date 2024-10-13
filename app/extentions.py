from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_admin import Admin
from flask_mail import Mail
from itsdangerous import URLSafeTimedSerializer
from .config import Config

db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
mail = Mail()
admin = Admin(name='MyAdmin', template_mode='bootstrap4')
s = URLSafeTimedSerializer(Config.SECRET_KEY)

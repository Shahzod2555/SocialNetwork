from datetime import datetime

from flask_login import UserMixin

from .publication import Publication
from .comment import Comment
from .like import Like
from ..extentions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    publication = db.relationship(Publication, backref='author_publication')
    comment = db.relationship(Comment, backref='author_comment')
    like = db.relationship(Like, backref='author_like', lazy='dynamic')
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email, phone) -> None:
        self.username: str = username
        self.password: str = password
        self.phone: str = phone
        self.email: str = email

    def __repr__(self):
        return '<User %r>' % self.username

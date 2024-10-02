from datetime import datetime

from flask_login import UserMixin

from .publication import Publication
from .comment import Comment
from .follow import Follower
from .like import Like
from ..extentions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String)
    publication = db.relationship(Publication, backref='author_publication', cascade='all, delete-orphan', passive_deletes=True)
    comment = db.relationship(Comment, backref='author_comment', cascade='all, delete-orphan', passive_deletes=True)
    like = db.relationship(Like, backref='author_like', cascade='all, delete-orphan', passive_deletes=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    password = db.Column(db.String(255), nullable=False)

    following = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower', lazy='dynamic')
    followers = db.relationship('Follower', foreign_keys='Follower.followed_id', backref='followed', lazy='dynamic')

    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email, phone, avatar) -> None:
        self.username: str = username
        self.password: str = password
        self.phone: str = phone
        self.email: str = email
        self.avatar: str = avatar

    def __repr__(self):
        return '<User %r>' % self.username


    def follow(self, user):
        if not self.is_following(user):
            new_follow = Follower(follower_id=self.id, followed_id=user.id)
            db.session.add(new_follow)

    def unfollow(self, user):
        follow = self.following.filter_by(followed_id=user.id).first()
        if follow:
            db.session.delete(follow)

    def is_following(self, user):
        return self.following.filter_by(followed_id=user.id).count() > 0

    def following_count(self):
        return self.following.count()

    def is_followed_by(self, user):
        return self.followers.filter_by(follower_id=user.id).count() > 0

    def followers_count(self):
        return self.followers.count()

    def publication_count(self):
        return Publication.query.filter_by(author=self.id).count()

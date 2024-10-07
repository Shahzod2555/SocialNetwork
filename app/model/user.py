from datetime import datetime
from email.policy import default

from flask_login import UserMixin

from .publication import Publication
from .comment import Comment
from .subscription import Subscription
from .like import Like
from .viewing import Viewing
from ..extentions import db, login_manager


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)

    publication = db.relationship(Publication, backref='author_publication', cascade='all, delete-orphan', passive_deletes=True)
    comment = db.relationship(Comment, backref='author_comment', cascade='all, delete-orphan', passive_deletes=True)
    like = db.relationship(Like, backref='author_like', cascade='all, delete-orphan', passive_deletes=True)
    viewing = db.relationship(Viewing, backref='author_viewing', cascade='all, delete-orphan', passive_deletes=True)

    username = db.Column(db.String(50), unique=True, nullable=False)
    phone = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    bio = db.Column(db.Text, nullable=True)
    avatar = db.Column(db.String, nullable=False, default="ava.svg")
    password = db.Column(db.String(255), nullable=False)

    subscription = db.relationship('Subscription', foreign_keys='Subscription.subscription_id', backref='subscription', lazy='dynamic')
    subscribers = db.relationship('Subscription', foreign_keys='Subscription.subscribers_id', backref='subscribers', lazy='dynamic')

    date_joined = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, username, password, email, phone, avatar) -> None:
        self.username: str = username
        self.password: str = password
        self.phone: str = phone
        self.email: str = email
        self.avatar: str = avatar

    def __repr__(self):
        return '<User %r>' % self.username


    def subscription_add(self, user):
        if not self.is_subscription(user):
            new_subscription = Subscription(subscription_id=self.id, subscribers_id=user.id)
            db.session.add(new_subscription)

    def un_subscription(self, user):
        subscription = self.subscription.filter_by(subscribers_id=user.id).first()
        if subscription:
            db.session.delete(subscription)

    def is_subscription(self, user):
        return self.subscription.filter_by(subscribers_id=user.id).count() > 0

    def subscription_count(self):
        return self.subscription.count()

    def is_subscribers_by(self, user):
        return self.subscribers.filter_by(subscription_id=user.id).count() > 0

    def subscribers_count(self):
        return self.subscribers.count()

    def publication_count(self):
        return Publication.query.filter_by(author=self.id).count()

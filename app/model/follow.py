from datetime import datetime

from ..extentions import db


class Follower(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    followed_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date_create = db.Column(db.DateTime, default=datetime.utcnow)

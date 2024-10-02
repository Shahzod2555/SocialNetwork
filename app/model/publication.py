from datetime import datetime

from .comment import Comment
from .like import Like

from ..extentions import db


class Publication(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'))
    likes = db.relationship(Like, backref='publication_like', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    comment = db.relationship(Comment, backref='publication_comment', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


    def like_count(self):
        return self.likes.count()

    def comment_count(self):
        return self.comment.count()

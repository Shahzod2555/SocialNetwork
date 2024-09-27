from ..model.comment import Comment
from ..forms import CommentAdd
from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..model.like import Like
from ..model.publication import Publication

main = Blueprint('main_blueprint', __name__)

@main.route('/')
@login_required
def index():
    publications = Publication.query.order_by(Publication.updated_at.desc()).all()

    user_likes = [like.publication for like in Like.query.filter_by(author=current_user.id).all()]
    comment = Comment.query.order_by(Comment.created_at.desc()).all()

    return render_template(
        template_name_or_list='main/index.html',
        publications=publications,
        user_likes=user_likes,
        form=CommentAdd(),
        comments=comment
    )
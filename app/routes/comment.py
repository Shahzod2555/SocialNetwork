from flask import Blueprint, redirect
from flask_login import login_required, current_user

from ..forms import CommentAdd
from ..extentions import db
from ..model.comment import Comment

comment_blueprint = Blueprint('comment_blueprint', __name__)

@comment_blueprint.route('/comment/<int:publication_id>', methods=['POST'])
@login_required
def comment(publication_id):
    form = CommentAdd()

    if form.validate_on_submit():
        author = current_user.id
        new_comment = Comment(author=author, content=form.content.data, publication=publication_id)

        try:
            db.session.add(new_comment)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
            return redirect('/')

    return redirect('/')
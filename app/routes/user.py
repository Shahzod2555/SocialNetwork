from flask import Blueprint, render_template
from flask_login import login_required, current_user

from ..forms import CommentAdd
from ..model.user import User
from ..functions import get_publication_data

user = Blueprint('user_blueprint', __name__)

@user.route('/profile')
@login_required
def profile():
    publications, user_likes, publication_comments = get_publication_data()

    return render_template(
        template_name_or_list='user/profile.html',
        publications=publications,
        user_likes=user_likes,
        form=CommentAdd(),
        publication_comment=publication_comments,
        author=current_user,
        following_count=current_user.following_count(),
        followers_count=current_user.followers_count(),
        publication_count=current_user.publication_count()
    )

@user.route('/user/<int:user_id>')
@login_required
def user_profile(user_id):
    publications, user_likes, publication_comments = get_publication_data(author_id=user_id)
    user_us = User.query.get_or_404(user_id)

    return render_template(
        template_name_or_list='user/user.html',
        publications=publications,
        user_likes=user_likes,
        form=CommentAdd(),
        publication_comment=publication_comments,
        author=user_us,
        following_count=user_us.following_count(),
        followers_count=user_us.followers_count(),
        publication_count = user_us.publication_count()
    )
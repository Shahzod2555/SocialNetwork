from flask import Blueprint, flash, redirect, url_for, request
from flask_login import login_required, current_user


from ..extentions import db
from ..model.user import User

subscription = Blueprint('subscription_blueprint', __name__)

@subscription.route('/follow/<int:user_id>', methods=['POST'])
@login_required
def subscription_user(user_id):
    user = User.query.get_or_404(user_id)
    if user == current_user:
        flash('Нельзя подписаться на самого себя!', 'danger')
        return redirect(request.referrer or url_for('user_blueprint.profile', user_id=user.id))

    if current_user.is_subscription(user):
        flash(f'Вы уже подписаны на {user.username}', 'info')
        return redirect(request.referrer or url_for('user_blueprint.profile', user_id=user.id))

    current_user.subscription_add(user)
    db.session.commit()
    flash(f'Вы подписались на {user.username}', 'success')
    return redirect(request.referrer or url_for('user_blueprint.profile', user_id=user.id))


@subscription.route('/unfollow/<int:user_id>', methods=['POST'])
@login_required
def un_subscription_user(user_id):
    user = User.query.get_or_404(user_id)

    if not current_user.is_subscription(user):
        flash(f'Вы не подписаны на {user.username}', 'info')
        return redirect(request.referrer or url_for('user_blueprint.profile', user_id=user.id))

    current_user.un_subscription(user)
    db.session.commit()
    flash(f'Вы отписались от {user.username}', 'success')
    return redirect(request.referrer or url_for('user_blueprint.profile', user_id=user.id))

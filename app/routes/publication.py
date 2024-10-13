from flask import Blueprint, render_template, request, redirect, flash
from ..functions import get_publication_data, save_media
from ..forms import PublicationCreate, PublicationUpdate
from flask_login import login_required, current_user
from ..model.publication import Publication
from ..forms import CommentAdd
from ..extentions import db


publication = Blueprint('publication_blueprint', __name__)


@publication.route('/publication/create', methods=['POST', 'GET'])
@login_required
def publication_create():
    form = PublicationCreate()

    if form.validate_on_submit():
        new_publication = Publication(
            title=form.title.data,
            author=current_user.id,
            content=form.content.data,
            hashtags=form.hashtags.data,
            is_published=form.is_publication.data,
            image=save_media(form.image.data, "SERVER_PATH_PUBLICATION_IMAGE") if form.image.data else None,
            video=save_media(form.video.data, "SERVER_PATH_PUBLICATION_VIDEO") if form.video.data else None,
            audio=save_media(form.audio.data, "SERVER_PATH_PUBLICATION_AUDIO") if form.audio.data else None,
            location=form.location.data,
            mentions=form.mentions.data,
        )

        try:
            db.session.add(new_publication)
            db.session.commit()
            return redirect(request.referrer or "/")
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
            flash("При создании публикации произошла ошибка", "danger")
            return redirect(request.referrer or "/")
    else:
        return render_template('publication/create.html', form=form)


@publication.route('/publication/update/<int:id_publication>',
                   methods=['POST', 'GET'])
@login_required
def publication_update(id_publication):
    publication_id = Publication.query.get_or_404(id_publication)
    form = PublicationUpdate()

    if publication_id.author == current_user.id:
        flash("У вас нет доступа к этой публикации", "danger")
        return redirect(request.referrer or "/")

    if request.method == 'GET':
        form.content.data = publication_id.content

    if form.validate_on_submit():
        publication_id.title = form.title.data
        publication_id.content = form.content.data
        publication_id.hashtags = form.hashtags.data
        publication_id.image = save_media(form.image.data, "SERVER_PATH_PUBLICATION_IMAGE") if form.image.data else publication_id.image
        publication_id.video = save_media(form.video.data, "SERVER_PATH_PUBLICATION_VIDEO") if form.video.data else publication_id.video
        publication_id.audio = save_media(form.audio.data, "SERVER_PATH_PUBLICATION_AUDIO") if form.audio.data else publication_id.audio
        publication_id.location = form.location.data
        publication_id.mentions = form.mentions.data

        try:
            db.session.add(publication_id)
            db.session.commit()
            return redirect(request.referrer or "/")
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
            flash("При обновлении публикации произошла ошибка", "danger")
            return redirect(request.referrer or "/")

    return render_template(
        'publication/update.html',
        form=form, publication_id=publication_id
    )


@publication.route(rule='/publication/delete/<int:id_publication>', methods=['POST', 'GET'])
@login_required
def publication_delete(id_publication):
    publication_id = Publication.query.get(id_publication)

    if publication_id.author == current_user.id:
        try:
            db.session.delete(publication_id)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
    else:
        return redirect('/'), flash("Соси хуй", "danger")


@publication.route(rule='/publication/<int:id_publication>',  methods=['POST', 'GET'])
def publication_view(id_publication):
    publication12 = Publication.query.get_or_404(id_publication)
    publication12.record_view(user_id=current_user.id)

    publications1, user_likes, publication_comments = get_publication_data(publications=[publication12])

    return render_template(
        template_name_or_list="publication/publication_view.html",
        publication=publication12,
        user_likes=user_likes,
        form=CommentAdd(),
        publication_comment=publication_comments,
        author=current_user
    )

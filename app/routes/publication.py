from flask import Blueprint, render_template, request, redirect, flash
from flask_login import login_required, current_user
from ..functions import get_publication_data, save_image_publication, save_video_publication, save_audio_publication
from ..forms import CommentAdd
from ..extentions import db
from ..forms import PublicationCreate, PublicationUpdate
from ..model.publication import Publication


publication = Blueprint('publication_blueprint', __name__)

@publication.route('/publication/create', methods=['POST', 'GET'])
@login_required
def create_publication():
    form = PublicationCreate()

    if form.validate_on_submit():

        if form.image.data:
            image = save_image_publication(form.image.data)
        else:
            image = None

        if form.video.data:
            video = save_video_publication(form.video.data)
        else:
            video = None

        if form.audio.data:
            audio = save_audio_publication(form.audio.data)
        else:
            audio = None

        new_publication = Publication(
            title=form.title.data,
            author=current_user.id,
            content=form.content.data,
            hashtags=form.hashtags.data,
            image=image,
            video=video,
            audio=audio,
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


@publication.route('/publication/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_publication(id):
    publication_id = Publication.query.get_or_404(id)
    form = PublicationUpdate()

    if publication_id.author != current_user:
        flash("У вас нет доступа к этой публикации", "danger")
        return redirect(request.referrer or "/")

    if request.method == 'GET':
        form.content.data = publication_id.content
        form.image.data = publication_id.image
        form.video.data = publication_id.video
        form.audio.data = publication_id.audio

    if form.validate_on_submit():
        if form.image.data:
            image = save_image_publication(form.image.data)
        else:
            image = None

        if form.video.data:
            video = save_video_publication(form.video.data)
        else:
            video = None

        if form.audio.data:
            audio = save_audio_publication(form.audio.data)
        else:
            audio = None

        publication_id.title = form.title.data
        publication_id.content = form.content.data
        publication_id.hashtags = form.hashtags.data
        publication_id.image = image if image else publication_id.image
        publication_id.video = video if video else publication_id.video
        publication_id.audio = audio if audio else publication_id.audio
        publication_id.location = form.location.data
        publication_id.mentions = form.mentions.data

        try:
            db.session.add(publication_id)
            db.session.commit()
            return redirect(request.referrer or "/")
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
            flash("При создании публикации произошла ошибка", "danger")
            return redirect(request.referrer or "/")

    return render_template(
        'publication/update.html',
        form=form, publication_id=publication_id
    )


@publication.route('/publication/delete/<int:id>', methods=['POST', 'GET'])
@login_required
def delete_publication(id):
    publication_id = Publication.query.get(id)
    try:
        db.session.delete(publication_id)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(f"Ошибка при создании публикации: {e}")


@publication.route('/publication/<int:id>', methods=['POST', 'GET'])
def publication_view(id):
    publication12 = Publication.query.get_or_404(id)
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

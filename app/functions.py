import os.path
import secrets
from flask import current_app
from PIL import Image

from .model.like import Like
from .model.comment import Comment
from .model.publication import Publication
from flask_login import current_user


def save_video_publication(video):
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(video.filename)
    video_fn = random_hex + f_ext
    video_path = os.path.join(current_app.config['SERVER_PATH_PUBLICATION_VIDEO'], video_fn)
    video.save(video_path)
    return video_fn


def save_audio_publication(audio):
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(audio.filename)
    audio_fn = random_hex + f_ext
    audio_path = os.path.join(current_app.config['SERVER_PATH_PUBLICATION_AUDIO'], audio_fn)
    audio.save(audio_path)
    return audio_fn


def save_image_publication(picture):
    random_hex = secrets.token_hex(12)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH_PUBLICATION_IMAGE'], picture_fn)
    picture.save(picture_path)
    i = Image.open(picture)
    i.save(picture_path)
    return picture_fn


def save_ava_picture(picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['SERVER_PATH_AVATAR'], picture_fn)
    output_size = (125, 125)
    i = Image.open(picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def get_publication_data(author_id=None, publications=None):
    if publications is None:
        if author_id is None:
            author_id = current_user.id
        publications = Publication.query.filter_by(author=author_id).order_by(Publication.updated_at.desc()).all()

    user_likes = {like.publication for like in Like.query.filter_by(author=current_user.id).all()}

    publication_comments = {
        publication.id: Comment.query.filter_by(publication=publication.id).order_by(Comment.created_at.desc()).all()
        for publication in publications
    }

    return publications, user_likes, publication_comments

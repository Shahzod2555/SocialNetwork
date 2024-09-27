from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from ..extentions import db
from ..model.publication import Publication

publication = Blueprint('publication_blueprint', __name__)

@publication.route('/publication/create', methods=['POST', 'GET'])
@login_required
def create_publication():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        author = current_user.id
        try:
            db.session.add(Publication(title=title, author=author, content=content))
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
    else:
        return render_template('publication/create.html')


@publication.route('/publication/update/<int:id>', methods=['POST', 'GET'])
@login_required
def update_publication(id):
    publication_id = Publication.query.get(id)
    if request.method == 'POST':
        publication_id.title, publication_id.content, publication_id.file = request.form.get('title'), request.form.get('content'), request.form.get('file')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(f"Ошибка при создании публикации: {e}")
    else:
        return render_template('publication/update.html', publication=publication_id)

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

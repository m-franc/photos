from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db

bp = Blueprint('blog', __name__)

# bp.add_url_rule('/', endpoint='index')

@bp.route('/')
def index():
    db = get_db()
    pictures = db.execute(
        'SELECT p.id, title, description, created, path, author_id, username'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    ).fetchall()
    return render_template('blog/index.html', pictures=pictures)

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        path = request.form['path']
        error = None
        if not title:
            error = 'Title is required.'
        if not path:
            error = 'Path is required.'
        if not description:
            error = 'Description is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO picture (title, description, path, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, path, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_picture(id, check_author=True):
    picture = get_db().execute(
        'SELECT p.id, title, description, path, created, author_id, username'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if picture is None:
        abort(404, f"Picture id {id} doesn't exist.")
    if check_author and picture['author_id'] != g.user['id']:
        abort(403)
    return picture

@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    picture = get_picture(id)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        path = request.form['path']
        error = None
        if not title:
            error = 'Title is required.'
        if not path:
            error = 'Path is required.'
        if not description:
            error = 'Description is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE picture SET title = ?, description = ?, path = ?'
                ' WHERE id = ?',
                (title, description, path, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', picture=picture)

@bp.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_picture(id)
    db = get_db()
    db.execute('DELETE FROM picture WHERE id = ?', (id))
    db.commit()
    return redirect(url_for('blog.index'))

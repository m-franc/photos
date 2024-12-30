import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort
from app.auth import login_required
from app.db import get_db
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS

UPLOAD_FOLDER = '/Users/maximefranc/Documents/projects/photos/app/static/pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'raf'}

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
    return jsonify(pictures)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None
        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if error is not None:
            flash(error)
        else:
            # check if the post request has the file part
            if 'path' not in request.files:
                flash('No file part')
                return redirect(url_for('blog.index'))
            file = request.files['path']
            # If the user does not select a file, the browser submits an
            # empty file without a filename.
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('blog.index'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                path = filename
            db = get_db()
            db.execute(
                'INSERT INTO picture (title, description, path, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, path, g.user['id'])
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/create.html')

def get_picture(id, show, check_author=True):
    picture = get_db().execute(
        'SELECT p.id, title, description, path, created, author_id, username'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()
    if picture is None:
        abort(404, f"Picture id {id} doesn't exist.")
    if show == 0:
        if check_author and picture['author_id'] != g.user['id']:
            abort(403)
    return picture

@bp.route('/<int:id>', methods=['GET'])
def show(id):
    picture = get_picture(id, 1)
    image = Image.open(UPLOAD_FOLDER + '/' + picture['path'])
    exifdata = image._getexif()
    return render_template('blog/show.html', picture=picture, exifdata=exifdata)


@bp.route('/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    picture = get_picture(id, 0)
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        error = None
        if not title:
            error = 'Title is required.'
        if not description:
            error = 'Description is required.'
        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE picture SET title = ?, description = ?'
                ' WHERE id = ?',
                (title, description, id)
            )
            db.commit()
            return redirect(url_for('blog.index'))
    return render_template('blog/update.html', picture=picture)

@bp.route('/<id>/delete', methods=['POST'])
@login_required
def delete(id):
    get_picture(id, 0)
    db = get_db()
    db.execute('DELETE FROM picture WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('blog.index'))

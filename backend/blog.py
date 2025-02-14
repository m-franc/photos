import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from backend.auth import login_required
from backend.db import get_db
from werkzeug.utils import secure_filename
from PIL import Image
from PIL.ExifTags import TAGS
import json

import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token, decode_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt, verify_jwt_in_request,
)

UPLOAD_FOLDER = '/Users/maximefranc/Documents/projects/photos/backend/static/pictures'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'raf'}

bp = Blueprint('blog', __name__, url_prefix='/blog/')

# bp.add_url_rule('/', endpoint='index')

@bp.before_request
def load_user():
    print("=== Debug Request ===")
    print(f"Method: {request.method}")
    print(f"Full URL: {request.url}")
    print(f"Base URL: {request.base_url}")
    print(f"Path: {request.path}")
    print(f"Script Root: {request.script_root}")
    print(f"Blueprint: {request.blueprint}")
    print(f"Endpoint: {request.endpoint}")
    print(f"URL Rule: {request.url_rule}")
    print("==================")

    # Vérifie si c'est vraiment une route de blog
    if not request.path.startswith('/blog'):
        print(f"⚠️ Warning: Non-blog route interceptée: {request.path}")
        return None
    g.user = None
    access_token = request.cookies.get("access_token_cookie")
    # print("📝 Token trouvé:", access_token)
    if not access_token:
        return abort(401, f"YOU NEED TO LOGIN")
    try:
        verify_jwt_in_request()
        # g.user = get_jwt_identity()
        claims = get_jwt()
        g.user = claims
        # print("User identité:", g.user['id'])
    except Exception as e:
        print("❌ Erreur JWT:", str(e))
        return abort(401, "Invalid token")

def sqlquery_to_array_of_object(query):
    columns = []

    rows = query.fetchall()
    data = []
    for col in query.description:
        columns.append(col[0])
    for row in rows:
        data.append(dict(zip(columns, row)))
    return data

@bp.route('/')
def index():
    db = get_db()
    pictures = db.execute(
        'SELECT p.id, title, description, created, path, author_id, username'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' ORDER BY created DESC'
    )
    # Create the columns of the json statam
    data = sqlquery_to_array_of_object(pictures)
    return json.dumps(data, indent=4, sort_keys=True, default=str)



def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.route('/create', methods=['GET', 'POST'])
# @login_required
def create():
    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        author_id = request.form['author_id']
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
            file = request.files.get("path")
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
                (title, description, path, author_id)
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
    # image = Image.open(UPLOAD_FOLDER + '/' + picture['path'])
    # exifdata = image._getexif()
    data = {
        "id": picture[0],
        "title": picture[1],
        "description": picture[2],
        "path": picture[3],
        "created": picture[4],
        "author_id": picture[5],
        "username": picture[6]
       }
    return json.dumps(data, indent=4, sort_keys=True, default=str)


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

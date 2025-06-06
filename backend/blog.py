import os
from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, current_app
)
from werkzeug.exceptions import abort
from auth import login_required
from db import get_db
from werkzeug.utils import secure_filename
from exif import Image
import json

import jwt
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token, decode_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies, get_jwt, verify_jwt_in_request,
)


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'pictures')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'raf'}

bp = Blueprint('blog', __name__, url_prefix='/blog/')

# bp.add_url_rule('/', endpoint='index')

@bp.before_request
def load_user():
    # Vérifie si c'est vraiment une route de blog
    print("BONJOUR !!!!!!!")
    if request.path.startswith('/blog/update'):
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
        print("User identité:", g.user['role'])
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
        'SELECT p.id, title, description, created, path, author_id, username,'
        ' m.brightness, m.date, m.aperture, m.zoom, m.speed'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' JOIN metadata m ON p.id = m.picture_id'
        ' ORDER BY m.date ASC'
    )

    # Create the columns of the json statam
    data = sqlquery_to_array_of_object(pictures)
    return json.dumps(data, indent=4, sort_keys=True, default=str)

@bp.route('/allmetadatas')
def allmetadatas():
    db = get_db()
    print("BONJOUR")
    metadatas = db.execute(
        'SELECT * FROM metadata'
    )
    # Create the columns of the json statam

    data = sqlquery_to_array_of_object(metadatas)
    return json.dumps(data, indent=4, sort_keys=True, default=str)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def insert_metadata(picture_id, metadata):
    print("PICTURE ID OOOH : ", picture_id)
    print("UN ELEMENT : ", metadata["brightness"])
    db = get_db()
    print("BONJOUR CEST PARTI")
    db.execute(
                'INSERT INTO metadata (picture_id, date, brightness, speed, zoom, aperture)'
                ' VALUES (?, ?, ?, ?, ?, ?)',
                (picture_id,
                 metadata["date"],
                 metadata["brightness"],
                 metadata["speed"],
                 metadata["zoom"],
                 metadata["aperture"])
            )
    db.commit()
    print("NORMALEMENT CEST BON")
    return None

def get_image_information(path):
    with open(os.path.join(UPLOAD_FOLDER, path), 'rb') as image_file:
        image_bytes = image_file.read()
    meta_data = Image(image_bytes)

    return {"date": meta_data.datetime_original,
            "brightness": meta_data.brightness_value,
            "speed": meta_data.exposure_time,
            "zoom": meta_data.focal_length,
            "aperture": meta_data.f_number}





@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    try:
        # Votre code d'upload actuel
        print("Chemin d'upload:", UPLOAD_FOLDER)
        print("Fichier reçu:", request.files)
        # etc.
    except Exception as e:
        print(f"Erreur détaillée: {str(e)}")
        print(f"Type d'erreur: {type(e)}")
        import traceback
        traceback.print_exc()
        return json.dumps({"error": str(e)}), 500
    if request.method == 'POST':
        print(f"UPLOAD_FOLDER est configuré à: {UPLOAD_FOLDER}")
        print(f"Chemin absolu: {os.path.abspath(UPLOAD_FOLDER)}")
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
            if 'path' not in request.files:
                flash('No file part')
                return redirect(url_for('blog.index'))
            file = request.files.get("path")
            if file.filename == '':
                flash('No selected file')
                return redirect(url_for('blog.index'))
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER, filename))
                path = filename
            db = get_db()

            cursor = db.execute(
                'INSERT INTO picture (title, description, path, author_id)'
                ' VALUES (?, ?, ?, ?)',
                (title, description, path, author_id)
            )
            db.commit()
            image_metadata = get_image_information(path)
            picture_id = cursor.lastrowid
            insert_metadata(picture_id, image_metadata)
        return json.dumps({"success": True, "message": "Post created successfully"}), 201
    return None

def get_picture(id, show, check_author=True):
    picture = get_db().execute(
        'SELECT p.id, title, description, path, created, author_id, username,'
        ' m.speed, m.zoom, m.brightness, m.aperture, m.date'
        ' FROM picture p JOIN user u ON p.author_id = u.id'
        ' JOIN metadata m ON p.id = m.picture_id'
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
    for elem in picture:
        print("ELEM : ", elem)
    data = {
        "id": picture[0],
        "title": picture[1],
        "description": picture[2],
        "path": picture[3],
        "created": picture[4],
        "author_id": picture[5],
        "username": picture[6],
        "speed": picture[7],
        "zoom": picture[8],
        "brightness": picture[9],
        "aperture": picture[10],
        "date": picture[11]
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

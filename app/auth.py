import functools
from collections.abc import Mapping

from flask import (
    Blueprint, make_response, flash, g, redirect, render_template, jsonify, request, session, url_for
)

from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    create_refresh_token,
    get_jwt_identity, set_access_cookies,
    set_refresh_cookies, unset_jwt_cookies
)

from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db



bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/')
def index():
    db = get_db()
    users = db.execute("SELECT * FROM user").fetchall()
    pictures = db.execute("SELECT * FROM picture").fetchall()
    return render_template('auth/index.html', users=users, pictures=pictures)

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':

        data = request.get_json()
        username = data['username']
        password = data['password']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data['username']
        password = data['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()
        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'
        if error is None:
            access_token = create_access_token(identity=user[1])
            response = make_response(jsonify({
                "user": {
                    "id": user[0],
                    "username": user[1]
                }
            }))
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )
            return response
        return jsonify(message="Invalid username or password"), 401
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout', methods=['POST'])
def logout():
    response = make_response(jsonify({"message": "Logged out successfully"}))
    response.set_cookie('access_token', '', expires=0, httponly=True, samesite='Lax')
    return response

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

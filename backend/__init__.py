import os
from dotenv import load_dotenv
from flask import (Flask, jsonify)

from . import db, auth, blog
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from backend.auth import bp as auth_bp
from backend.blog import bp as blog_bp

jwt = JWTManager()

def create_app(test_config=None):
    # create and configure the app

    app = Flask(__name__, instance_relative_config=True)
    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Exception occurred: {str(e)}")
        return jsonify(error=str(e)), 500

    app.config['JWT_TOKEN_LOCATION'] = ['cookies']
    # Only allow JWT cookies to be sent over https. In production, this
    # should likely be True
    app.config['JWT_COOKIE_SECURE'] = False
    app.config['JWT_COOKIE_SAMESITE'] = "Lax"
    app.config['JWT_COOKIE_HTTPONLY'] = True
    # Set the cookie paths, so that you are only sending your access token
    # cookie to the access endpoints, and only sending your refresh token
    # to the refresh endpoint. Technically this is optional, but it is in
    # your best interest to not send additional cookies in the request if
    # they aren't needed.
    app.config['JWT_ACCESS_COOKIE_PATH'] = '/'
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    app.config['JWT_COOKIE_CSRF_PROTECT'] = True
    # Set the secret key to sign the JWTs with
    load_dotenv
    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Change this!

    jwt.init_app(app)

    CORS(app, resources={
        r"/*": {  # Permet l'accès à toutes les routes
            "origins": [
                "http://localhost:3000",  # URL de votre frontend Next.js
                "http://127.0.0.1:3000"   # Alternative URL
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
    })
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )


    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    app.register_blueprint(auth_bp)
    app.register_blueprint(blog_bp)
    app.add_url_rule('/', endpoint="index")
    return app

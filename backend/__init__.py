import os
from dotenv import load_dotenv
from flask import (Flask, jsonify)

from . import db
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from auth import bp as auth_bp
from blog import bp as blog_bp

from datetime import timedelta

jwt = JWTManager()

def create_app(test_config=None):
    # create and configure the app



    app = Flask(__name__, instance_relative_config=True)
    @app.errorhandler(Exception)
    def handle_exception(e):
        print(f"Exception occurred: {str(e)}")
        return jsonify(error=str(e)), 500

    # @app.after_request
    # def add_cors_headers(response):
    #     response.headers['Access-Control-Allow-Origin'] = '*'
    #     response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
    #     response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    #     return response

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
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=24)
    app.config['JWT_REFRESH_COOKIE_PATH'] = '/token/refresh'
    # Enable csrf double submit protection. See this for a thorough
    # explanation: http://www.redotheweb.com/2015/11/09/api-security.html
    app.config['JWT_COOKIE_CSRF_PROTECT'] = False
    # Set the secret key to sign the JWTs with
    load_dotenv()
    app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET_KEY')

    jwt.init_app(app)

    CORS(app, resources={
        r"/*": {  # Permet l'accès à toutes les routes
            "origins":[
                "http://localhost:3000",
                "http://frontend:3000",
                "http://frontend-server-1:3000"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        },
    })
    instance_path = app.instance_path
    db_path = os.path.join(instance_path, 'app.sqlite')
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(instance_path, 'app.sqlite'),
    )
    print(f"Trying to access database at: {db_path}")
    print(f"Database file exists: {os.path.exists(db_path)}")
    print(f"Database file is readable: {os.access(db_path, os.R_OK)}")
    print(f"Database file is writable: {os.access(db_path, os.W_OK)}")
    print(f"Instance path: {instance_path}")

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

    return app

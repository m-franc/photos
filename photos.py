from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///photos.db"
# initialize the app with the extension
db.init_app(app)


@app.route("/")
def index():
    return "<p>Hello, World!</p>"

@app.route("/photos")
def photos():
    return "<p>Pictures there in the futre</p>"

@app.route("/photos/<id>")
def show_photo(id):
    return f"<p>Photo n° {escape(id)}</p>"

with app.test_request_context():
    print(url_for('index'))
    print(url_for('photos'))
    print(url_for('show_photo', id=":id"))

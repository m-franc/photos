from flask import Flask
from markupsafe import escape
from flask import url_for

app = Flask(__name__)

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

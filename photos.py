from flask import Flask
from markupsafe import escape

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/photos")
def photos():
    return "<p>Pictures there in the futre</p>"

@app.route("/photo/<int:id>")
def show_photo(id):
    return f"<p>Photo n° {escape(id)}</p>"

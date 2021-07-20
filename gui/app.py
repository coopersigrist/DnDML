from flask import Flask, render_template, request, session
from flask_session import Session
from markupsafe import escape
import os
import math

TEMPLATE_DIR = os.path.abspath('templates')
STATIC_DIR = os.path.abspath('static')

app = Flask(__name__, template_folder=TEMPLATE_DIR, static_folder=STATIC_DIR)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

@app.route("/", methods = ["GET", "POST"])
def home():
    if request.method == "POST":
        print("Received: ")
        print(request.get_json())
        return 'OK', 200
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
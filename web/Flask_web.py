from flask import Flask, render_template
#err ref: https://stackoverflow.com/questions/50905636/e0401unable-to-import-flask/50905745
#Go to Command Palette using [Ctrl + Shift + P]. select python:select interpreter and then choose your appropriate virtualenv.
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)

app.config.from_object(Config)

@app.route ("/")
def index():
    paragraphs = [
        "Section 1",
        "Section 2",
        "Section 3"
    ]
    # title = "Flask Web"
    # return"hello world"
    return render_template("index.html", title = "home", data = paragraphs) #title = title


@app.route("/N")
def index2():
    return "hello"

if __name__ == "__main__":
    app.run(debug = True,  host = "0.0.0.0.", port = 3000) 
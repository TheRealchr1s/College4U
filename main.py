from flask import Flask
import flask
import os
import requests
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from cllg.cllg import get_sheet

app = Flask(__name__)
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

@app.route("/")
def index():
    return flask.render_template("index.html")

@app.route("/info", methods=["POST"])
def info_page():
    cllg_list = flask.request.form["cllg"].split("\n")
    names = get_sheet(cllg_list)
    return flask.render_template("info.html", cllgnames=names)

@app.route("/dl")
def dl():
    return flask.send_file("cllg/colleges.xlsx")
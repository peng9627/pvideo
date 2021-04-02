# coding=utf-8
import importlib

from pycore.data.entity import config
from flask import Blueprint, session, redirect, render_template

from api import index, movie

api = Blueprint('api', __name__, template_folder='../templates', static_folder='../resources')


@api.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Methods'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = '*'
    headers = []
    if 'auth' in environ.headers:
        headers.append('auth')
    if 'auth_key' in environ.headers:
        headers.append('auth_key')
    if len(headers) > 0:
        environ.headers['Access-Control-Expose-Headers'] = ','.join(headers)
    environ.headers['Server'] = 'dami_server'
    return environ


@api.route('/<module>/<method>', methods=['POST'])
def module_method(module, method):
    mod = importlib.import_module("api." + module)
    return getattr(mod, method)()


@api.route('/download/<code>', methods=['GET'])
def download_id(code):
    session["code"] = code
    return redirect('/download')


@api.route('/download', methods=['GET'])
def download():
    if "code" in session:
        code = session["code"]
    else:
        code = ""
    return render_template('/download.html', code=code, android_url=config.get("server", "android_url"),
                           ios_url=config.get("server", "ios_url"))


@api.route('/play_movie')
def play_movie():
    return movie.play()

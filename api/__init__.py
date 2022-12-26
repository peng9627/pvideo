# coding=utf-8
import importlib

from flask import Blueprint, session, redirect, render_template, request
from pycore.data.entity import config
from pycore.utils import http_utils

from api import index, movie

api = Blueprint('api', __name__, template_folder='../templates', static_folder='../resources')


@api.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Methods'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = '*'
    print(request.url)
    headers = []
    if 'auth' in environ.headers:
        headers.append('auth')
    if 'auth_key' in environ.headers:
        headers.append('auth_key')
    if len(headers) > 0:
        environ.headers['Access-Control-Expose-Headers'] = ','.join(headers)
    environ.headers['Server'] = 'dami_server'
    return environ


@api.route('/', methods=['GET'])
def index():
    return redirect(config.get("server", "download_url"))


@api.route('/<module>/<method>', methods=['POST'])
def module_method(module, method):
    mod = importlib.import_module("api." + module)
    return getattr(mod, method)()


@api.route('/download/<code>', methods=['GET'])
def download_id(code):
    if 'MICROMESSENGER' in http_utils.get_user_agent(request.headers.environ):
        return render_template('/download_we.html')
    session["code"] = code
    return redirect('/download')


@api.route('/download', methods=['GET'])
def download():
    if 'MICROMESSENGER' in http_utils.get_user_agent(request.headers.environ):
        return render_template('/download_we.html')
    if "code" in session:
        code = session["code"]
    else:
        code = ""
    return render_template('/download.html', code=code,
                           share_url=config.get("server", "download_url") + "/" + code,
                           android_url=config.get("server", "android_url"), ios_url=config.get("server", "ios_url"),
                           h5_url=config.get("server", "h5_url"))


@api.route('/play_movie.m3u8')
def play_movie():
    return movie.play()


@api.route('/get_url')
def get_url():
    return movie.get_url()


@api.route('/movie.key')
def movie_key():
    return movie.get_key()

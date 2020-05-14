# coding=utf-8
import importlib

from pycore.data.entity import config
from flask import Blueprint, session, redirect, render_template

api = Blueprint('api', __name__, template_folder='../templates', static_folder='../resources')


@api.after_request
def cors(environ):
    environ.headers['Access-Control-Allow-Origin'] = '*'
    environ.headers['Access-Control-Allow-Method'] = '*'
    environ.headers['Access-Control-Allow-Headers'] = '*'
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
        code = "10000"
    return render_template('/download.html', code=code, android_url=config.get("server", "android_url"),
                           ios_url=config.get("server", "ios_url"))

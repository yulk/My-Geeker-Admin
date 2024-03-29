from flask import Blueprint, render_template, send_from_directory
from flask_jwt_extended import jwt_required

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    return render_template('index.html')


@index_bp.route('/favicon.ico')
def fav_icon():
    return send_from_directory(directory='static', path='favicon.ico')

from flask import Blueprint, Flask

from .v3_admin_vite_api import v3_api
from .table_api import table_api
from .user_api import user_api
from .geeker_admin_api import geeker_admin_api


def register_apis(app: Flask):
    apis = Blueprint('api', __name__, url_prefix='/api/v1')

    apis.register_blueprint(v3_api)
    apis.register_blueprint(table_api)
    apis.register_blueprint(user_api)
    apis.register_blueprint(geeker_admin_api)

    app.register_blueprint(apis)

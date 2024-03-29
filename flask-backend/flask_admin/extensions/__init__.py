from flask import Flask

from .init_db import db, migrate
from .init_jwt import jwt
from .init_upload import init_upload


def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    init_upload(app)

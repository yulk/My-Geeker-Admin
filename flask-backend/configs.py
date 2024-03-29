import os
from datetime import timedelta


class BaseConfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'flask-admin-simple')

    # FLASK_UPLOADS 设置
    UPLOADS_DEFAULT_DEST = 'upload'
    UPLOADED_PHOTOS_DEST = 'upload/photos'
    UPLOADED_EXCELS_DEST = 'upload/excels'
    UPLOADED_WORDS_DEST = 'upload/words'
    UPLOADS_AUTOSERVE = True

    # SQLALCHEMY 数据库设置
    SQLALCHEMY_DATABASE_URI = None
    # 通过SQLALCHEMY_BINDS，可以设置同时连接多个数据库
    # SQLALCHEMY_BINDS = {
    #     # 'flask_admin@sqlite': 'sqlite:///flask_admin.db',
    #     # 'flask_admin@mysql': 'mysql+pymysql://root:Flask2023@127.0.0.1:3306/flask_admin',
    #     # 'flask_admin@pgsql': 'postgresql+psycopg://yulik:Flask#2021@127.0.0.1:5432/flask_admin',
    #     # 'flask_admin@mssql': 'mssql+pymssql://<username>:<password>@<freetds_name>/?charset=utf8',
    # }
    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

    JWT_TOKEN_LOCATION = ['headers', 'cookies']
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=9)


class DevelopmentConfig(BaseConfig):
    """开发配置"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///flask_admin.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestingConfig(BaseConfig):
    """测试配置"""

    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # 内存数据库


class ProductionConfig(BaseConfig):
    """生成环境配置"""

    SQLALCHEMY_DATABASE_URI = 'mysql://root:root@127.0.0.1:3306/flask_admin'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


config = {'dev': DevelopmentConfig, 'test': TestingConfig, 'prod': ProductionConfig}

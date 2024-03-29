from flask import Flask, render_template
from flask_uploads import IMAGES, UploadSet, configure_uploads
from configs import config
from flask_admin.apis import register_apis
from flask_admin.extensions import register_extensions
from flask_admin.cmdlines import register_cmdlines
from flask_admin.orms import UserORM
from flask_admin.views import register_views
from flask_cors import CORS


def create_app(config_name='dev'):
    app = Flask('flask-admin-simple')

    app.config.from_object(config[config_name])
    app.json.ensure_ascii = False  # 解决flask 反回中文是unicode编码 https://blog.csdn.net/yutu75/article/details/131156819
    register_extensions(app)  # 注册扩展,包括db/upload/jwt
    register_cmdlines(app)
    register_apis(app)

    CORS(
        app, supports_credentials=True, origins='*', resources=r'/*'
    )  # origins='http://example.com'

    register_views(app)

    @app.errorhandler(403)
    def handle_404(e):
        return render_template('error/403.html')

    @app.errorhandler(404)
    def handle_403(e):
        return render_template('error/404.html')

    @app.errorhandler(500)
    def handle_500(e):
        return render_template('error/500.html')

    return app

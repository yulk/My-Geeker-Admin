from collections import OrderedDict
from copy import deepcopy
import os
from flask import (
    Blueprint,
    make_response,
    redirect,
    render_template,
    request,
    jsonify,
    Response,
    current_app,
)
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_current_user,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_access_cookies,
    unset_refresh_cookies,
    get_jwt_identity,
)
import json

from flask_uploads import extension
from flask_admin.extensions import db
from flask_admin.orms import UserORM
from flask_cors import cross_origin
from flask_admin.extensions.init_upload import photos, excels, words
from flask import send_from_directory, url_for, abort
import pandas as pd
from io import BytesIO


geeker_admin_api = Blueprint('geeker_admin', __name__)


def json2response(jsonfilename):
    root = current_app.config.get('ROOT_PATH')
    json_file_path = os.path.join(root, 'static', 'json', jsonfilename)

    try:
        # 打开并加载JSON文件
        with open(json_file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        print(data)
        # 使用 jsonify 返回 JSON 格式的数据
        return jsonify(data)

    except FileNotFoundError:
        # 如果文件未找到，则返回错误信息
        return jsonify({'error': 'The specified JSON file was not found.'}), 404

    except Exception as e:
        # 其他任何读取或解析JSON文件时的错误
        return jsonify(
            {'error': f'An error occurred while reading the JSON file: {str(e)}.'}
        ), 500


@geeker_admin_api.post('/login')
def login_in():
    data = request.get_json()

    # {'username': 'admin', 'password': '12345678', 'code': '1234567'}
    print(data)
    user: UserORM = db.session.execute(
        db.select(UserORM).where(UserORM.username == data['username'])
    ).scalar()

    if not user:
        return {'msg': '用户不存在', 'code': -1}, 401
    if not user.check_password(data['password']):
        # user.password = '12345678'
        return {'msg': '用户密码错误', 'code': -1}, 401
    print(user.json())

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response = make_response(
        {'code': 200, 'data': {'access_token': access_token}, 'msg': '登录成功'}
    )

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


@geeker_admin_api.route('/logout', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def logout():
    response = make_response({'code': 200, 'msg': '成功'})
    # unset_access_cookies(response)
    # unset_refresh_cookies(response)
    return response


@geeker_admin_api.route('/menu/list', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def menulist():
    return json2response('authMenuList.json')


@geeker_admin_api.route('/auth/buttons', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def authbuttons():
    return json2response('authButtonList.json')


# /user   GET
@geeker_admin_api.route('/user/status', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_status():
    return json2response('user_status.json')


@geeker_admin_api.route('/user/gender', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_gender():
    return json2response('user_gender.json')


@geeker_admin_api.route('/user/department', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_department():
    return json2response('user_department.json')


@geeker_admin_api.route('/user/role', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_role():
    return json2response('user_role.json')


# user_list
@geeker_admin_api.route('/user/list', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_list():
    return json2response('user_list.json')


# user / edit
@geeker_admin_api.route('/user/edit', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_edit():
    # [TODO]未做真实的修改,直接把提交的请求数据返回
    if request.method == 'OPTIONS':
        return make_response({'code': 200, 'msg': 'OK'})
    data = request.get_json()
    print('user_edit[TODO]未做真实的修改,直接把提交的请求数据返回')
    return make_response({'code': 200, 'data': data, 'msg': '修改成功'})


@geeker_admin_api.route('/user/delete', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_delete():
    # [TODO]未做真实的删除,直接把提交的请求数据返回
    if request.method == 'OPTIONS':
        return make_response({'code': 200, 'msg': 'OK'})
    data = request.get_json()
    print('user_delete[TODO]未做真实的删除,直接把提交的请求数据返回')
    return make_response({'code': 200, 'data': data, 'msg': '删除成功'})


# user / rest_password
@geeker_admin_api.route('/user/rest_password', methods=['GET', 'OPTIONS', 'POST'])
@geeker_admin_api.route('/user/change', methods=['GET', 'OPTIONS', 'POST'])
@geeker_admin_api.route('/user/add', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def fake_response():
    # [TODO]未做真实的删除,直接把提交的请求数据返回
    if request.method == 'OPTIONS':
        return make_response({'code': 200, 'msg': 'OK'})
    data = request.get_json()
    print('user_delete[TODO]未做真实的删除,直接把提交的请求数据返回', data)
    return make_response({'code': 200, 'data': data, 'msg': '删除成功'})


@geeker_admin_api.route('/user/tree/list', methods=['GET', 'OPTIONS', 'POST'])
# @cross_origin()
def user_tree_list():
    return json2response('user_tree_list.json')


# 生成文件下载
@geeker_admin_api.route('/user/export', methods=['GET', 'POST'])
def export_user_data():
    df = pd.DataFrame(
        {
            'id': [
                '188809847655516924',
                '...',
            ],
            'username': [
                '吴秀兰',
                '...',
            ],
            # 其他字段...
        }
    )

    # 使用pandas将DataFrame保存为Excel (xlsx格式)
    excel_buffer = BytesIO()
    df.to_excel(excel_buffer, index=False, engine='openpyxl')

    # 重置缓冲区指针到开始位置
    excel_buffer.seek(0)

    # 创建HTTP响应，设置Content-Type和Content-Disposition头
    response = make_response(excel_buffer.read())
    response.headers['Content-Disposition'] = 'attachment; filename=user_data.xlsx'
    response.headers[
        'Content-Type'
    ] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    print('response', response)

    return response


# upload/img
@geeker_admin_api.route('/file/upload/img', methods=['GET', 'POST'])
def upload_img():
    print('api.geeker_admin.show 上传的文件信息', request.files)
    # ImmutableMultiDict([('file', <FileStorage: 'PixPin_2024-03-20_10-17-26.png' ('image/png')>)])
    if request.method == 'POST' and 'file' in request.files:
        print(
            '上传的文件名',
            request.files['file'].filename,
            # 'extension',
            # extension(request.files['file'].filename),
            # 'secure_filename',
            # secure_filename(request.files['file'].filename),
            # 这个函数有BUG，会去掉文件中所有的中文信息
        )

        # 这里如果不传name进去，它会去掉文件名里的中文，所以从请求中拿到中文文件名后，直接传入，防止被改名
        filename = photos.save(
            request.files['file'], name=request.files['file'].filename
        )

        # from flask_uploads.UploadSet import url
        fileUrl = photos.url(filename)
        print('存储的文件URL', fileUrl)

        # 如果自己建服务
        # fileUrl = url_for(
        #     'api.geeker_admin.show',  # 下面那个API： @geeker_admin_api.route('/show/<setname>/<filename>') 的链接地址
        #     setname=photos.name,
        #     filename=filename,
        #     _external=True,  # 使用绝对URL
        # )
        # 这里不做 redirect(URL) 防止前台申请看到 304 跳转后直接报错, 直接返回JSON包，带fileUrl

        return make_response(
            {
                'code': 200,
                'data': {'fileUrl': fileUrl},
                'msg': '上传成功',
            }
        )
    return render_template('upload.html')


# 自己建上传图文显示的服务
# @geeker_admin_api.route('/show/<setname>/<filename>')
# def show(setname, filename):
#     config = current_app.upload_set_config.get(setname)  # type: ignore
#     if config is None:
#         return {'msg': f'upload_set_config{setname}不存在', 'code': -1}, 404
#     return send_from_directory(config.destination, filename)


# user/import EXCEL 上传
@geeker_admin_api.route('/user/import', methods=['GET', 'POST'])
def upload_excel():
    print('api.geeker_admin.show 上传的文件信息', request.files)
    # ImmutableMultiDict([('file', <FileStorage: 'PixPin_2024-03-20_10-17-26.png' ('image/png')>)])
    if request.method == 'POST' and 'file' in request.files:
        print('上传的文件名', request.files['file'].filename)

        # 这里如果不传name进去，它会去掉文件名里的中文，所以从请求中拿到中文文件名后，直接传入，防止被改名
        # 这个函数有BUG，会去掉文件中所有的中文信息, 碰到 全中文(不带任何英文数字)的文件名会报错
        filename = excels.save(
            request.files['file'], name=request.files['file'].filename
        )

        # from flask_uploads.UploadSet import url
        fileUrl = excels.url(filename)
        print('存储的文件URL', fileUrl)

        # 如果自己建服务
        # fileUrl = url_for(
        #     'api.geeker_admin.show',  # 下面那个API： @geeker_admin_api.route('/show/<setname>/<filename>') 的链接地址
        #     setname=photos.name,
        #     filename=filename,
        #     _external=True,  # 使用绝对URL
        # )
        # 这里不做 redirect(URL) 防止前台申请看到 304 跳转后直接报错, 直接返回JSON包，带fileUrl

        return make_response(
            {
                'code': 200,
                'data': {'fileUrl': fileUrl},
                'msg': '上传成功',
            }
        )
    return render_template('upload.html')

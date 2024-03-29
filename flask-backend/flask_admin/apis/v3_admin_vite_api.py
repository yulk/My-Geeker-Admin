from collections import OrderedDict
from copy import deepcopy

from flask import Blueprint, make_response, redirect, request, jsonify, Response
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

from flask_admin.extensions import db
from flask_admin.orms import UserORM
from flask_cors import cross_origin
# from flask_admin.plus import vieCode
# # 生成验证码
# def get_captcha():
#     image, code = vieCode().GetCodeImage()
#     code = ''.join(code).lower()
#     out = BytesIO()
#     session['code'] = code
#     image.save(out, 'png')
#     out.seek(0)
#     resp = make_response(out.read())
#     resp.content_type = 'image/png'
#     return resp, code


v3_api = Blueprint('passport', __name__)


@v3_api.route('/login/code', methods=['OPTIONS', 'GET'])
# @cross_origin()
def login_code():
    response = make_response(
        {
            'code': 200,
            'data': 'http://127.0.0.1:5000/static/captcha.gif',
            'msg': '验证码',
        }
    )
    print(response)
    return response


@v3_api.post('/users/login')
# @cross_origin()
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

    access_token = create_access_token(user)
    refresh_token = create_refresh_token(user)

    response = make_response(
        {'code': 200, 'data': {'access_token': access_token}, 'msg': '登录成功'}
    )

    set_access_cookies(response, access_token)
    set_refresh_cookies(response, refresh_token)

    return response


# 先通过OPTIONS请求获取请求头，再通过POST请求获取请求体
@v3_api.route('/users/info', methods=['OPTIONS'])
def user_info_options():
    response = make_response(
        {
            'code': 200,
            'msg': '我在',
        }
    )
    return response


@v3_api.get('/users/info')
@jwt_required()
def user_info():
    current_user: UserORM = get_current_user()
    print(
        current_user, current_user.username, current_user.nickname, current_user.roles
    )
    # current_user = get_jwt_identity()
    response = make_response(
        {
            'code': 200,
            'data': {
                'username': current_user.username,
                'roles': current_user.roles.split('|'),
            },
            'msg': '获取用户详情成功',
        }
    )
    print(response)
    return response


# Protect a route with jwt_required, which will kick out requests
# without a valid JWT present.
@v3_api.route('/protected', methods=['GET'])
@jwt_required()
def protected():
    # Access the identity of the current user with get_jwt_identity
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# {'code': 200, 'data': {'token': string}, 'msg': '登录成功'}


@v3_api.route('/users/logout', methods=['GET', 'POST'])
@jwt_required()
def users_logout():
    response = make_response(redirect('/login'))
    unset_access_cookies(response)
    unset_refresh_cookies(response)
    return response

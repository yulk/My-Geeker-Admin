from flask import Blueprint, request, jsonify
from flask_sqlalchemy.pagination import Pagination

from flask_admin.extensions import db
from flask_admin.orms import TableORM
from flask_admin.schemas import TableSchema
from datetime import datetime

user_api = Blueprint('user', __name__)


@user_api.get('/user/tree/list')
@user_api.get('/user/list')
def user_list():
    page = request.args.get('currentPage', default=1, type=int)
    per_page = request.args.get('size', default=10, type=int)

    _type = request.args.get('type', 'normal')
    ret = []
    if _type == 'tree':
        dept_obj: TableORM = TableORM.query.get(1)
        for child in dept_obj.children:
            child_data = child.json()
            child_data['children'] = []
            if child.children:
                child_data['isParent'] = True
            for son in child.children:
                son_data = son.json()
                # son_data["isParent"] = True
                child_data['children'].append(son_data)
            ret.append(child_data)
        return {'code': 200, 'msg': '请求权限数据成功', 'data': ret}
    q = db.select(TableORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)
    userschema = TableSchema()
    return jsonify(
        {
            'code': 200,
            'data': {
                'total': 100,
                # 'list': [item.json() for item in pages.items],
                'list': [userschema.dump(item) for item in pages.items],
            },
            'msg': '获取表格数据成功',
        }
    )


# {
#     'createTime': '1990-05-17 23:43:36',
#     'email': 's.bpvuv@uqjefku.ee',
#     'id': '510000198605217752',
#     'phone': '17514765412',
#     'roles': 'editor',
#     'status': true,
#     'username': 'Margaret Hall',
# }
@user_api.put('/user')
def change_user():
    data = request.get_json()
    rid = data['id']

    user_obj = TableORM.query.get(rid)
    for k, v in data.items():
        if k == 'password':
            user_obj.password = v
        elif k == 'createTime':
            user_obj.createTime = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            # "1990-05-17 23:43:36"
        else:
            setattr(user_obj, k, v or None)
    user_obj.save()
    return jsonify({'code': 200, 'data': {}, 'msg': '修改成功'})


@user_api.delete('/user/<int:rid>')
def del_user_rid(rid):
    user_obj = TableORM.query.get(rid)
    user_obj.delete()
    return jsonify({'code': 200, 'msg': '删除删除成功'})


# @user_api.post('/user')
# def create_user():
#     data = request.get_json()
#     if data['id']:
#         del data['id']
#     user = TableORM(**data)
#     user.save()
#     return {'code': 200, 'msg': '新增部门成功'}


# @user_api.put('/user/<int:rid>')
# def change_user_rid(rid):
#     data = request.get_json()
#     del data['id']

#     user_obj = TableORM.query.get(rid)
#     for key, value in data.items():
#         setattr(user_obj, key, value)
#     user_obj.save()
#     return {'code': 200, 'msg': '修改部门成功'}


# @user_api.delete('/user/<int:rid>')
# def del_user_rid(rid):
#     user_obj = TableORM.query.get(rid)
#     user_obj.delete()
#     return {'code': 200, 'msg': '删除删除成功'}

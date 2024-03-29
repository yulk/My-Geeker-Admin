from flask import Blueprint, request, jsonify
from flask_sqlalchemy.pagination import Pagination

from flask_admin.extensions import db
from flask_admin.orms import TableORM
from flask_admin.schemas import TableSchema
from datetime import datetime

table_api = Blueprint('table', __name__)


@table_api.get('/table')
def table_list():
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
        return {'code': 0, 'message': '请求权限数据成功', 'data': ret}
    q = db.select(TableORM)

    pages: Pagination = db.paginate(q, page=page, per_page=per_page)
    tableschema = TableSchema()
    return jsonify(
        {
            'code': 0,
            'data': {
                'total': 100,
                # 'list': [item.json() for item in pages.items],
                'list': [tableschema.dump(item) for item in pages.items],
            },
            'message': '获取表格数据成功',
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
@table_api.put('/table')
def change_table():
    data = request.get_json()
    rid = data['id']

    table_obj = TableORM.query.get(rid)
    for k, v in data.items():
        if k == 'password':
            table_obj.password = v
        elif k == 'createTime':
            table_obj.createTime = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
            # "1990-05-17 23:43:36"
        else:
            setattr(table_obj, k, v or None)
    table_obj.save()
    return jsonify({'code': 0, 'data': {}, 'message': '修改成功'})


@table_api.delete('/table/<int:rid>')
def del_table_rid(rid):
    table_obj = TableORM.query.get(rid)
    table_obj.delete()
    return jsonify({'code': 0, 'message': '删除删除成功'})


# @table_api.post('/table')
# def create_table():
#     data = request.get_json()
#     if data['id']:
#         del data['id']
#     table = TableORM(**data)
#     table.save()
#     return {'code': 0, 'message': '新增部门成功'}


# @table_api.put('/table/<int:rid>')
# def change_table_rid(rid):
#     data = request.get_json()
#     del data['id']

#     table_obj = TableORM.query.get(rid)
#     for key, value in data.items():
#         setattr(table_obj, key, value)
#     table_obj.save()
#     return {'code': 0, 'message': '修改部门成功'}


# @table_api.delete('/table/<int:rid>')
# def del_table_rid(rid):
#     table_obj = TableORM.query.get(rid)
#     table_obj.delete()
#     return {'code': 0, 'message': '删除删除成功'}

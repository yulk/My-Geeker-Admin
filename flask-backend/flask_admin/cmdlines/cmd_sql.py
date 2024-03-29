import csv
import os
import json
from flask import Flask, current_app
from datetime import datetime
from flask_admin.extensions import db
from flask_admin.orms import (
    UserORM,
    TableORM,
    PhotoORM,
    DictTypeORM,
    DictDataORM,
    PowerORM,
    RoleORM,
    RolePowerORM,
    UserRoleORM,
    dict_table2orm,
)

from flask_admin.schemas import (
    UserRoleSchema,
    RolePowerSchema,
    UserSchema,
    RoleSchema,
    PowerSchema,
    PhotoSchema,
    TableSchema,
    DictDataSchema,
    DictTypeSchema,
)

from sqlalchemy.sql import table, column, select, insert, delete, func


def dict_to_orm(d, o):
    for k, v in d.items():
        if k == 'password':
            o.password = v
        elif k in ['createTime', 'update_time', 'create_time'] and v:
            # print(v)
            if len(v) <= len('1990-05-17 23:43:36'):
                setattr(o, k, datetime.strptime(v, '%Y-%m-%d %H:%M:%S') or None)
            else:
                setattr(o, k, datetime.strptime(v, '%Y-%m-%d %H:%M:%S.%f') or None)
        else:
            setattr(o, k, v or None)


def csv_to_databases(path, orm):
    with open(path, encoding='utf-8') as file:
        for d in csv.DictReader(file):
            o = orm()
            dict_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()


def json_to_databases(path, orm):
    with open(path, encoding='utf-8') as file:
        for d in json.load(file)['data']['list']:
            o = orm()
            dict_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()


def json_to_databases_puredata(path, orm):
    with open(path, encoding='utf-8') as file:
        for d in json.load(file):
            print(d)
            o = orm()
            dict_to_orm(d, o)
            db.session.add(o)
            db.session.flush()
        db.session.commit()


def add_user_role():
    admin_role = RoleORM.query.filter_by(id=1).first()
    admin_user = UserORM.query.filter_by(id=1).first()
    admin_user.role.append(admin_role)
    test_role = RoleORM.query.filter_by(id=2).first()
    test_user = UserORM.query.filter_by(id=2).first()
    test_user.role.append(test_role)
    db.session.commit()


def select_one_from_orm(orm):
    # stmt = orm.select()
    # result = db.session.execute(db.select(orm).filter_by(id=1)).scalar_one_or_none()
    result = orm.query.first()

    print(result)


def select_cnt_orm(orm):
    stmt = select(orm)
    result_proxy = db.session.execute(stmt)
    query_result = result_proxy.scalars().all()
    # 获取记录条数
    print(f'Total records in {orm} {len(query_result)} rows')


def del_orm(orm):
    stmt = delete(orm)
    result = db.session.execute(stmt)
    print(f'Deleted {result.rowcount} rows')
    db.session.commit()


def inst_orm(path, orm):
    with open(path, encoding='utf-8') as file:
        data = json.load(file)
        # 下面逐行插入
        # for d in json.load(file):
        #     stmt = orm.insert().values(d)
        stmt = orm.insert().values(data)  # 一次性插入 many insert
        # print(stmt)
        result = db.session.execute(stmt)
        print(f'Inserted {result.rowcount} rows')
        db.session.flush()
        db.session.commit()


def register_script_sql(app: Flask):
    @app.cli.command('sql')
    def sql_table():
        # root = current_app.config.get('ROOT_PATH')

        # print(RolePowerTBL.c)
        # print(UserRoleTBL.c)
        # print(select(RolePowerTBL))
        # print(insert(RolePowerTBL))

        # role_power_file = os.path.join(root, 'static', 'data', 'role_power.json')

        # rolepower = {'id': 1, 'power_id': 13, 'role_id': 2}
        # # print(UserSchema().fields)
        # print(RolePowerSchema().fields.keys())
        # res = RolePowerSchema(load_instance=False).load(rolepower)
        # print(rolepower, res)

        for v in dict_table2orm.values():
            select_cnt_orm(v)
            select_one_from_orm(v)

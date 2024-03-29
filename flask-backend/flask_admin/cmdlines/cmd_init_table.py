import csv
import os
import json
from pprint import pprint
from flask import Flask, current_app
from datetime import datetime

from marshmallow import ValidationError
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
    dict_table2schema,
    dict_schema2orm,
)


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


def schema2db(filepath, SchemaName):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # schema = SchemaName(many=True)
        try:
            loads = SchemaName(many=True).load(data)
        except ValidationError as err:
            pprint(err.messages)
        print(f'{SchemaName.__name__} Inserted {len(loads)} rows')
        db.session.add_all(loads)
        db.session.commit()


def schema2dbbyORM(filepath, SchemaName):
    with open(filepath, 'r', encoding='utf-8') as file:
        data = json.load(file)
        # schema = SchemaName(many=True)
        try:
            loads = SchemaName(load_instance=False, many=True).load(data)
        except ValidationError as err:
            pprint(err.messages)
        # print(SchemaName.__name__)
        # print(dict_schema2orm.get(SchemaName.__name__))
        stmt = dict_schema2orm.get(SchemaName.__name__).insert().values(loads)
        result = db.session.execute(stmt)
        print(f'{SchemaName.__name__} Inserted {result.rowcount} rows')
        db.session.flush()
        db.session.commit()


def register_script_init_table(app: Flask):
    @app.cli.command('init_table')
    def init_table():
        db.drop_all()
        db.create_all()

        root = current_app.config.get('ROOT_PATH')

        # user 表有密码需要处理
        user_data_path = os.path.join(root, 'static', 'data', 'ums_user.csv')
        csv_to_databases(user_data_path, UserORM)

        for item in ['table', 'role', 'power', 'photo', 'role_power', 'user_role']:
            data_path = os.path.join(root, 'static', 'data', f'{item}.json')
            schema2db(data_path, dict_table2schema.get(item))

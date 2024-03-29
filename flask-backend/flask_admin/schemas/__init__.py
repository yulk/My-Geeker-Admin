from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, SQLAlchemyAutoSchemaOpts
# from marshmallow_sqlalchemy import SQLAlchemySchemaOpts, SQLAlchemySchema

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

from flask_admin.extensions import db


dict_schema2orm = {
    'UserSchema': UserORM,
    'PowerSchema': PowerORM,
    'RoleSchema': RoleORM,
    'TableSchema': TableORM,
    'PhotoSchema': PhotoORM,
    'DictTypeSchema': DictTypeORM,
    'DictDataSchema': DictDataORM,
    'UserRoleSchema': RolePowerORM,  # 改用ORM
    'RolePowerSchema': UserRoleORM,  # 同上
}


class BaseOpts(SQLAlchemyAutoSchemaOpts):
    # https://marshmallow-sqlalchemy.readthedocs.io/en/latest/recipes.html
    # Base Schema II
    def __init__(self, meta, ordered=False):
        if not hasattr(meta, 'sqla_session'):
            meta.sqla_session = db.session
        if not hasattr(meta, 'include_relationships') and hasattr(meta, 'model'):
            meta.include_relationships = True
        if not hasattr(meta, 'include_fk'):
            meta.include_fk = True
        if not hasattr(meta, 'load_instance'):
            meta.load_instance = True
        super(BaseOpts, self).__init__(meta, ordered=ordered)
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        # include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表
        # load_instance = True  # 是否将查询结果转换为对象 AuthorSchema(load_instance=False)
        # transient = True #瞬态对象创建


class BaseSchema(SQLAlchemyAutoSchema):
    # SQLAlchemyAutoSchema： 自动生成 SQLAlchemy 模型的模式
    OPTIONS_CLASS = BaseOpts


class UserSchema(BaseSchema):
    class Meta:
        model = UserORM
        # include_relationships = True


class TableSchema(BaseSchema):
    class Meta:
        model = TableORM
        # include_fk = True


class PhotoSchema(BaseSchema):
    class Meta:
        model = PhotoORM  # table = models.Album.__table__


# 2024-04-22 通义灵码 AI 生成：
# 按照这个格式为 DictTypeORM, DictDataORM, PowerORM, RolePowerORM, RoleORM,，UserRoleORM 也生成对应的 Schema 类
class DictTypeSchema(BaseSchema):
    class Meta:
        model = DictTypeORM
        # include_relationships = True
        # load_instance = True


class DictDataSchema(BaseSchema):
    class Meta:
        model = DictDataORM
        # include_relationships = True
        # load_instance = True


class PowerSchema(BaseSchema):
    class Meta:
        model = PowerORM
        # include_relationships = True
        # load_instance = True


class RoleSchema(BaseSchema):
    class Meta:
        model = RoleORM
        # include_relationships = True
        # load_instance = True


# 改用ORM -- TABLE no more


class UserRoleSchema(BaseSchema):
    class Meta:
        model = UserRoleORM
        # table = UserRoleTBL  改用ORM


class RolePowerSchema(BaseSchema):
    class Meta:
        model = RolePowerORM
        # table = RolePowerTBL 改用ORM


dict_table2schema = {
    'user': UserSchema,
    'table': TableSchema,
    'photo': PhotoSchema,
    'dicttype': DictTypeSchema,
    'dictdata': DictDataSchema,
    'power': PowerSchema,
    'role': RoleSchema,
    'role_power': RolePowerSchema,
    'user_role': UserRoleSchema,
}

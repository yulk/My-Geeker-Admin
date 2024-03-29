from flask_admin.extensions import db
from ._base import BaseORM


# 创建中间表
class RolePowerORM(BaseORM):
    __tablename__ = 'role_power'  # 中间表名称
    id = db.Column(
        'id', db.Integer, primary_key=True, autoincrement=True, comment='标识'
    )  # 主键
    power_id = db.Column(
        'power_id', db.Integer, db.ForeignKey('power.id'), comment='用户编号'
    )  # 属性 外键
    role_id = db.Column(
        'role_id', db.Integer, db.ForeignKey('role.id'), comment='角色编号'
    )  # 属性 外键


# Table 'role_power' is already defined for this MetaData instance
# RolePowerTBL = db.Table(
#     'role_power',  # 中间表名称
#     BaseORM.metadata,
#     db.Column(
#         'id', db.Integer, primary_key=True, autoincrement=True, comment='标识'
#     ),  # 主键
#     db.Column(
#         'power_id', db.Integer, db.ForeignKey('power.id'), comment='用户编号'
#     ),  # 属性 外键
#     db.Column(
#         'role_id', db.Integer, db.ForeignKey('role.id'), comment='角色编号'
#     ),  # 属性 外键
# )

from flask_admin.extensions import db
from ._base import BaseORM


class UserRoleORM(BaseORM):
    __tablename__ = 'user_role'
    id = db.Column(
        'id', db.Integer, primary_key=True, autoincrement=True, comment='标识'
    )
    user_id = db.Column(
        'user_id', db.Integer, db.ForeignKey('user.id'), comment='用户编号'
    )
    role_id = db.Column(
        'role_id', db.Integer, db.ForeignKey('role.id'), comment='角色编号'
    )


# UserRoleTBL = db.Table(
#     'user_role',  # 中间表名称
#     BaseORM.metadata,
#     db.Column(
#         'id', db.Integer, primary_key=True, autoincrement=True, comment='标识'
#     ),  # 主键
#     db.Column(
#         'user_id', db.Integer, db.ForeignKey('user.id'), comment='用户编号'
#     ),  # 属性 外键
#     db.Column(
#         'role_id', db.Integer, db.ForeignKey('role.id'), comment='角色编号'
#     ),  # 属性 外键
# )

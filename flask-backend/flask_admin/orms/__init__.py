from flask_admin.extensions import db

from .user import UserORM
from .table import TableORM
from .photo import PhotoORM
from .dict import DictTypeORM, DictDataORM
from .power import PowerORM
from .role import RoleORM
from .role_power import RolePowerORM
from .user_role import UserRoleORM

# PowerORM,RoleORM,RolePowerORM,UserRoleORM,PhotoORM

dict_table2orm = {
    'user': UserORM,
    'table': TableORM,
    'photo': PhotoORM,
    'dicttype': DictTypeORM,
    'dictdata': DictDataORM,
    'power': PowerORM,
    'role': RoleORM,
    'role_power': RolePowerORM,
    'user_role': UserRoleORM,
}

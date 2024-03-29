from ._base import BaseORM
from datetime import datetime
from typing import List, Optional

from sqlalchemy import ForeignKey, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship


class TableORM(BaseORM):
    __tablename__ = 'table'
    id: Mapped[String] = mapped_column(String(18), primary_key=True, comment='身份证')
    username: Mapped[String] = mapped_column(String(50), comment='名字')
    phone: Mapped[String] = mapped_column(String(32), nullable=False, comment='手机')
    email: Mapped[String] = mapped_column(String(64), nullable=False, comment='邮箱')
    roles: Mapped[String] = mapped_column(String(64), nullable=False, comment='角色')
    status: Mapped[Boolean] = mapped_column(
        Boolean, comment='状态(True开启,False关闭)', default=True
    )
    createTime: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        comment='创建时间',
        default=datetime.now,
    )

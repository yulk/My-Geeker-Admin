from flask_admin.extensions import db
from sqlalchemy import inspect


class BaseORM(db.Model):
    __abstract__ = True

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        # 获取当前模型的所有列名和值
        mapper = inspect(self.__class__)
        columns = [
            c.key for c in mapper.columns if not c.key.startswith('password')
        ]  # 过滤掉以 'password' 开头的项
        values = {col: getattr(self, col) for col in columns}

        # 将所有字段和值转换为字符串形式，便于拼接输出
        field_values = ', '.join([f'{k}={v!r}' for k, v in values.items()])

        return f'<{self.__class__.__name__}({field_values})>'

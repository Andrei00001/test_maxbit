import sqlalchemy as sa
from sqlalchemy import ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class UserModel(Base):
    __tablename__ = 'users'

    id = sa.Column(sa.BIGINT, primary_key=True)
    name = sa.Column(sa.String(50))
    login = sa.Column(sa.String(50), unique=True)


class TaskModel(Base):
    __tablename__ = 'tasks'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    user_id = sa.Column(sa.BIGINT, ForeignKey('users.id'))
    name = sa.Column(sa.String(50))
    description = sa.Column(sa.String(255))
    state = sa.Column(sa.Boolean, default=False, server_default='false')

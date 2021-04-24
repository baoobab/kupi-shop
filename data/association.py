import sqlalchemy
from sqlalchemy import orm

from .db_session import SqlAlchemyBase


class Association(SqlAlchemyBase):
    __tablename__ = 'association'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    user_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    favs_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    orders_id = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    o_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
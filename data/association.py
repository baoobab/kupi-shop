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

    def __init__(self, user_id, favs_id, orders_id, o_count):
        self.user_id = user_id
        self.favs_id = favs_id
        self.orders_id = orders_id
        self.o_count = o_count
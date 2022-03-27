import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Author(SqlAlchemyBase):
    __tablename__ = 'authors'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    photo = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    songs = orm.relationship("Song", secondary="links")



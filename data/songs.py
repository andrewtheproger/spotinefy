import sqlalchemy
from .db_session import SqlAlchemyBase
from sqlalchemy import orm


class Song(SqlAlchemyBase):
    __tablename__ = 'songs'

    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    duration = sqlalchemy.Column(sqlalchemy.Integer)
    clip = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    year = sqlalchemy.Column(sqlalchemy.Integer)
    authors = orm.relationship("Author", secondary="links")


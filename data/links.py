import sqlalchemy
from .db_session import SqlAlchemyBase


class Link(SqlAlchemyBase):
    __tablename__ = 'links'
    author_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('authors.id'),
        primary_key=True)
    song_id = sqlalchemy.Column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey('songs.id'),
        primary_key=True)
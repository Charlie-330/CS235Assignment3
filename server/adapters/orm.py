from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime, Float,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from server.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

comments = Table(
    'comments', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_rank', ForeignKey('movies.rank')),
    Column('comment', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

# Rank,Title,Genre,Description,Director,Actors,Year,Runtime (Minutes),Rating,Votes,Revenue (Millions),Metascore,poster
movies = Table(
    'movies', metadata,
    Column('rank', Integer, primary_key=True, autoincrement=True),
    Column('title', String(255), nullable=False),
    Column('genre', String(255), nullable=False),
    Column('description', String(1024), nullable=False),
    Column('director', String(255), nullable=False),
    Column('actors', String(255), nullable=False),
    Column('year', Integer, nullable=False),
    Column('runtime', Integer, nullable=False),
    Column('rating', Float, nullable=False),
    Column('vote', Integer, nullable=False),
    Column('revenue', Float, nullable=False),
    Column('metascore', Float, nullable=False),
    Column('poster', String(255), nullable=True)
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_comments': relationship(model.Comment, backref='_user')
    })
    mapper(model.Comment, comments, properties={
        '_comment': comments.c.comment,
        '_timestamp': comments.c.timestamp
    })
    mapper(model.Movie, movies, properties={
        '_rank': movies.c.rank,
        '_year': movies.c.year,
        '_title': movies.c.title,
        '_description': movies.c.description,
        '_director': movies.c.director,
        '_actors': movies.c.actors,
        '_comments': relationship(model.Comment, backref='_movie'),
        '_genre': movies.c.genre,
        '_runtime': movies.c.runtime,
        '_rating': movies.c.rating,
        '_vote': movies.c.vote,
        '_revenue': movies.c.revenue,
        '_metascore': movies.c.metascore,
        '_poster': movies.c.poster,
    })

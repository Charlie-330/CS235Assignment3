import csv
import os

from datetime import date
from typing import List
from sqlalchemy import and_
from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from server.domain.model import User, Movie, Comment
from server.adapters.repository import AbstractRepository


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self) -> List[Movie]:
        movies = None
        try:
            movies = self._session_cm.session.query(Movie).all()
        except NoResultFound:
            # Ignore any exception and return None.
            pass
        return movies

    def get_movie_by_rank(self, rank: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._rank == rank).one()
        except NoResultFound:
            pass
        return movie

    def get_movie_by_query(self, actor_name: str, genre_name: str, director_name: str):
        if actor_name == "*":
            actor_name = ''
        if genre_name == "*":
            genre_name = ''
        if director_name == "*":
            director_name = ''
        movies = self._session_cm.session.query(Movie).filter(
            Movie._actors.like("%" + actor_name + "%"),
            Movie._genre.like("%" + genre_name + "%"),
            Movie._director.like("%" + director_name + "%"),
           ).all()

        return movies

    def get_comments(self) -> List[Comment]:
        comments = self._session_cm.session.query(Comment).all()
        return comments

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        with self._session_cm as scm:
            scm.session.add(comment)
            scm.commit()


def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            movie_data = row
            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]
            yield movie_data


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global tags
    tags = dict()

    insert_movies = """
        INSERT INTO movies (
        rank,title,genre,description,director,actors,year,runtime,rating,vote,revenue,metascore,poster)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, '1000MoviesWithPoster.csv')))

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_comments = """
        INSERT INTO comments (
        id, user_id, movie_rank, comment, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_comments, generic_generator(os.path.join(data_path, 'comments.csv')))

    conn.commit()
    conn.close()


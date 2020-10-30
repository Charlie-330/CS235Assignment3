import abc
from typing import List
from datetime import date

from server.domain.model import User, Comment, Movie


repo_instance = None


class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.

        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """" Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self):
        """ Returns all the movie
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_rank(self, rank: int):
        """ Returns one movie by rank"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_by_query(self, actor_name: str, genre_name: str, director_name: str):
        """ Returns one movie by rank"""
        raise NotImplementedError

    @abc.abstractmethod
    def add_comment(self, comment: Comment):
        """ Adds a Comment to the repository.

        If the Comment doesn't have bidirectional links with an comment and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if comment.user is None or comment not in comment.user.comments:
            raise RepositoryException('Comment not correctly attached to a User')
        if comment.movie is None or comment not in comment.movie.comments:
            raise RepositoryException('Comment not correctly attached to an Movie')

    @abc.abstractmethod
    def get_comments(self):
        """ Returns the Comments stored in the repository. """
        raise NotImplementedError








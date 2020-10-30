from typing import Iterable

from server.adapters.repository import AbstractRepository
from server.domain.model import make_comment, Comment, Movie


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_comment(comment_text: str, username: str, repo: AbstractRepository, movie_rank: int):
    # Check that the movie exists.
    movie = repo.get_movie_by_rank(movie_rank)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    print(user, username)
    if user is None:
        raise UnknownUserException

    # Create comment.
    comment = make_comment(comment_text, user, movie)
    print(comment)

    # Update the repository.
    repo.add_comment(comment)


def get_movie(repo: AbstractRepository):
    movies = repo.get_movie()
    count = len(movies)
    return movies_to_dict(movies), count


def get_movie_by_rank(repo: AbstractRepository, rank: int):
    movie = repo.get_movie_by_rank(rank)
    return movie_to_dict(movie)


def get_movie_by_query(repo:AbstractRepository, actor_name: str, genre_name: str, director_name: str):
    movies = repo.get_movie_by_query(actor_name, genre_name, director_name)
    count = len(movies)
    return movies_to_dict(movies), count


def movie_to_dict(movie: Movie):
    movie_dict = {
        'rank': movie.rank,
        'year': movie.year,
        'title': movie.title,
        'description': movie.description,
        'director': movie.director,
        'actors': movie.actors,
        'comments': comments_to_dict(movie.comments),
        'genre': movie.genre,
        'runtime': movie.runtime,
        'rating': movie.rating,
        'vote': movie.vote,
        'revenue': movie.revenue,
        'metascore': movie.metascore,
        'poster': movie.poster
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def comment_to_dict(comment: Comment):
    comment_dict = {
        'username': comment.user.username,
        'movie_rank': comment.movie.rank,
        'comment_text': comment.comment,
        'timestamp': comment.timestamp
    }
    return comment_dict


def comments_to_dict(comments: Iterable[Comment]):
    return [comment_to_dict(comment) for comment in comments]

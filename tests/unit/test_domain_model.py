from datetime import date

from server.domain.model import User, make_comment, ModelException, Movie

import pytest


@pytest.fixture()
def movie():
    return Movie(
    2016,'title', 'description', 'director', 'actors', 'genre', 100,
    8.9, 123, 123.3, 111, 8, "sss"
    )


@pytest.fixture()
def user():
    return User('dbowie', '1234567890')


def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie 1234567890>'

    for comment in user.comments:
        # User should have an empty list of Comments after construction.
        assert False


def test_movie_construction(movie):
    assert movie.rank == 8
    assert movie.year == 2016
    assert movie.title == "title"
    assert movie.description == 'description'
    assert movie.director == "director"
    assert movie.actors == 'actors'
    assert movie.genre == 'genre'
    assert movie.runtime == 100
    assert movie.vote == 123
    assert movie.metascore == 111

    assert repr(movie) == '<Movie 2016 title>'


def test_make_comment_establishes_relationships(user, movie):
    comment_text = 'top 1000 movies!'
    comment = make_comment(comment_text, user, movie)

    # Check that the User object knows about the Comment.
    assert comment in user.comments

    # Check that the Comment knows about the User.
    assert comment.user is user

    # Check that Movies knows about the Comment.
    assert comment in movie.comments

    # Check that the Comment knows about the movie.
    assert comment.movie is movie



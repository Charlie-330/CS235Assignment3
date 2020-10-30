from datetime import date, datetime
from typing import List, Iterable


class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._comments: List[Comment] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def comments(self) -> Iterable['Comment']:
        return iter(self._comments)

    def add_comment(self, comment: 'Comment'):
        self._comments.append(comment)

    def __repr__(self) -> str:
        return f'<User {self._username} {self._password}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username


class Comment:
    def __init__(
            self, user: User, comment: str, timestamp: datetime, movie: 'Movie'
    ):
        self._user: User = user
        self._movie: Movie = movie
        self._comment: str = comment
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def comment(self) -> str:
        return self._comment

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Comment):
            return False
        return other._user == self._user and other._comment == self._comment and other._timestamp == self._timestamp and other._movie == self._movie


class Movie:
    def __init__(
            self, year: int, title: str, description: str,
            director: str, actors: str, genre: str, runtime: int,
            rating: float, vote: int, revenue: float, metascore: int,
            rank: int, poster: str
    ):
        self._rank: int = rank
        self._year: int = year
        self._title: str = title
        self._description: str = description
        self._director: str = director
        self._actors: str = actors
        self._comments: List[Comment] = list()
        self._genre: str = genre
        self._runtime: int = runtime
        self._rating: float = rating
        self._vote: int = vote
        self._revenue: float = revenue
        self._metascore: int = metascore
        self._poster: str = poster

    @property
    def poster(self) -> str:
        return self._poster

    @property
    def rank(self) -> int:
        return self._rank

    @property
    def year(self) -> int:
        return self._year

    @property
    def title(self) -> str:
        return self._title

    @property
    def description(self) -> str:
        return self._description

    @property
    def director(self) -> str:
        return self._director

    @property
    def actors(self) -> str:
        return self._actors

    @property
    def comments(self) -> Iterable[Comment]:
        return iter(self._comments)

    @property
    def number_of_comments(self) -> int:
        return len(self._comments)

    @property
    def genre(self) -> str:
        return self._genre

    @property
    def runtime(self) -> int:
        return self._runtime

    @property
    def rating(self) -> float:
        return self._rating

    @property
    def vote(self) -> int:
        return self._vote

    @property
    def revenue(self) -> float:
        return self._revenue

    @property
    def metascore(self) -> int:
        return self._metascore

    def add_comment(self, comment: Comment):
        self._comments.append(comment)

    def __repr__(self):
        return f'<Movie {self.year} {self._title}>'


class ModelException(Exception):
    pass


def make_comment(comment_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    comment = Comment(user, comment_text, timestamp, movie)
    user.add_comment(comment)
    movie.add_comment(comment)

    return comment


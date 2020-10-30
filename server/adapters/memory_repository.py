import csv
import os
import re
from datetime import date, datetime

from werkzeug.security import generate_password_hash

from server.adapters.repository import AbstractRepository, RepositoryException
from server.domain.model import User, Comment, Movie, make_comment


class MemoryRepository(AbstractRepository):
    def __init__(self):
        self._users = list()
        self._comments = list()
        self._movies = list()

    def add_user(self, user: User):
        self._users.append(user)

    def get_user(self, username) -> User:
        return next((user for user in self._users if user.username == username), None)

    def add_movie(self, movie: Movie):
        self._movies.append(movie)

    def get_movie(self):
        return self._movies

    def get_movie_by_rank(self, rank: int) -> Movie:
        rank = max(1,min(rank, len(self._movies)))
        movie = None
        try:
            movie = self._movies[rank-1]
        except Exception:
            pass  # Ignore exception and return None.
        return movie

    def get_movie_by_query(self, actor_name: str, genre_name: str, director_name: str):
        movies = []
        for x in self._movies:
            flag1 = 1
            flag2 = 1
            flag3 = 1
            if actor_name != "*":
                flag1 = re.search(actor_name, x.actors, re.IGNORECASE)
            if genre_name != "*":
                flag2 = re.search(genre_name, x.genre, re.IGNORECASE)
            if director_name != "*":
                flag3 = re.search(director_name, x.director, re.IGNORECASE)
            if flag1 is not None and flag2 is not None and flag3 is not None:
                movies.append(x)
        return movies

    def add_comment(self, comment: Comment):
        super().add_comment(comment)
        self._comments.append(comment)

    def get_comments(self):
        return self._comments


def read_csv_file(filename: str):
    with open(filename, encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]
            yield row


def load_movies(data_path: str, repo: MemoryRepository):
    for data_row in read_csv_file(os.path.join(data_path, '1000MoviesWithPoster.csv')):
        movie = Movie(
            rank=data_row[0],
            title=data_row[1],
            genre=data_row[2],
            description=data_row[3],
            director=data_row[4],
            actors=data_row[5],
            year=data_row[6],
            runtime=data_row[7],
            rating=data_row[8],
            vote=data_row[9],
            revenue=data_row[10],
            metascore=data_row[11],
            poster=data_row[12],
        )

        # Add the Article to the repository.
        repo.add_movie(movie)


def load_users(data_path: str, repo: MemoryRepository):
    users = dict()

    for data_row in read_csv_file(os.path.join(data_path, 'users.csv')):
        user = User(
            username=data_row[1],
            password=generate_password_hash(data_row[2])
        )
        repo.add_user(user)
        users[data_row[0]] = user
    return users


def load_comments(data_path: str, repo: MemoryRepository, users):
    for data_row in read_csv_file(os.path.join(data_path, 'comments.csv')):
        comment = make_comment(
            comment_text=data_row[3],
            user=users[data_row[1]],
            movie=repo.get_movie_by_rank(int(data_row[2])),
            timestamp=datetime.fromisoformat(data_row[4]),
        )
        repo.add_comment(comment)


def populate(data_path: str, repo: MemoryRepository):
    # load movies into the repository
    load_movies(data_path, repo)

    # Load users into the repository.
    users = load_users(data_path, repo)

    # Load comments into the repository.
    load_comments(data_path, repo, users)



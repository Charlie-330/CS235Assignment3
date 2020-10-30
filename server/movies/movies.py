from datetime import date
import math
from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import server.adapters.repository as repo
import server.movies.services as services

from server.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)


@movies_blueprint.route('/movies', methods=['GET'])
def movies():

    page = request.args.get('page')
    actor_name = request.args.get('actor_name')
    genre_name = request.args.get('genre_name')
    director_name = request.args.get('director_name')
    if actor_name is None or actor_name == "":
        actor_name = '*'
    if genre_name is None or genre_name == "":
        genre_name = '*'
    if director_name is None or director_name == "":
        director_name = '*'
    movies, count = services.get_movie_by_query(repo.repo_instance,actor_name,genre_name,director_name)
    total = math.ceil(count/5)
    if page is None:
        page = 1
    else:
        page = max(min(int(page), total), 1)

    movies = movies[(page-1)*5: min(page*5, count)]
    current_start = max(math.ceil(page/5)*5 - 4, 1)
    end = min(current_start + 4, total)
    return render_template(
        'movies/movies.html',
        movies=movies,
        page=page,
        current_start=current_start,
        end=end,
        total=total,
        actor_name=actor_name,
        genre_name=genre_name,
        director_name=director_name,
        count=count

    )


@movies_blueprint.route('/movie/detail', methods=['GET', 'POST'])
def detail():
    rank = request.args.get('rank')

    if rank is None:
        rank = 1
    else:
        rank = max(1, int(rank))
    movies, count = services.get_movie(repo.repo_instance)

    form = CommentForm()
    if form.validate_on_submit():
        username = session.get('username', "")
        movie_rank = rank
        # Use the service layer to store the new comment.
        try:
            services.add_comment(form.comment.data, username, repo.repo_instance, movie_rank)
        except services.UnknownUserException:
            return redirect(
                url_for('authentication_bp.login2',)
            )



    movie = services.get_movie_by_rank(repo.repo_instance, rank)
    comment_len = len(movie['comments'])
    form.comment.data = ""
    return render_template(
        'movies/detail.html',
        movie=movie,
        rank=rank,
        count=count,
        form=form,
        comment_len=comment_len,
    )

class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', [
        DataRequired(),
        Length(min=4, message='Your comment is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    submit = SubmitField('Post submit')
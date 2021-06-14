import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from database.models import setup_db, db_drop_and_create_all, Actor, Movie
from flask_cors import CORS
from auth.auth import AuthError, requires_auth


def create_app(test_config=None):
    
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # Set up CORS. Allow '*' for origins.
    CORS(app, resources={'/': {'origins': '*'}})

    # db_drop_and_create_all()

    @app.after_request
    def after_request(response):
        """ Set Access Control """

        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type, Authorization, true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET, POST, PATCH, DELETE, OPTIONS')

        return response

    @app.route('/')
    def home():
        return jsonify({
            'success': True
        }), 200

    @app.route('/movies')
    @requires_auth('get:movies')
    def get_all_movies(payload):
        movies_query = Movie.query.order_by(Movie.id).all()
        return jsonify({
            'success': True,
            'movies': [movie.format() for movie in movies_query]
        }), 200

    @app.route('/movies/<int:id>')
    @requires_auth('get:movies-details')
    def get_movie_by_id(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie(payload):
        try:
            request_body = request.get_json()

            if 'title' not in request_body \
                or 'release_date' not in request_body \
                    or 'cast' not in request_body:
                raise ValueError

            new_movie = Movie(
                request_body.get('title'),
                request_body.get('release_date')
            )

            actors = Actor.query.filter(Actor.name.in_(
                request_body.get('cast'))).all()

            if len(request_body.get('cast')) == len(actors):
                new_movie.cast = actors
                new_movie.insert()
            else:
                abort(422)

        except ValueError:
            abort(422)

        except Exception as e:
            print(e)
            abort(500)

        return jsonify({
            'success': True,
            'movie_id': new_movie.id
        }), 200

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movie(payload, id):
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            request_body = request.get_json()
            if 'title' in request_body:
                if request_body.get('title') == "":
                    raise ValueError
                movie.title = request_body.get('title')

            if 'release_date' in request_body:
                if request_body.get('release_date') == "":
                    raise ValueError
                movie.release_date = request_body.get('release_date')

            if 'cast' in request_body:
                if len(request_body.get('cast')) == 0:
                    raise ValueError

                actors = Actor.query.filter(
                    Actor.name.in_(request_body.get('cast'))
                ).all()

                if len(actors) == len(request_body.get('cast')):
                    movie.cast = actors
                else:
                    raise ValueError

            movie.update()

        except ValueError:
            abort(422)

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()
        if movie is None:
            abort(404)

        try:
            movie.delete()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'movie_id': id
        }), 200

    @app.route('/actors')
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actor.query.order_by(Actor.id).all()

        return jsonify({
            'success': True,
            'actors': [actor.format() for actor in actors]
        }), 200

    @app.route('/actors/<int:id>')
    @requires_auth('get:actors-details')
    def get_actor_by_id(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()
        if actor is None:
            abort(404)

        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_actors(payload):
        try:
            request_body = request.get_json()

            if 'name' not in request_body \
                or 'age' not in request_body \
                    or 'gender' not in request_body:
                abort(422)

            new_actor = Actor(
                request_body.get('name'),
                request_body.get('age'),
                request_body.get('gender')
            )

            new_actor.insert()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'actor_id': new_actor.id
        }), 200

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actors(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            request_body = request.get_json()

            if 'name' in request_body:
                if request_body.get('name') == "":
                    raise ValueError
                actor.name = request_body.get('name')

            if 'age' in request_body:
                if request_body.get('age') <= 0:
                    raise ValueError
                actor.age = request_body.get('age')

            if 'gender' in request_body:
                if request_body.get('gender').lower() not in \
                        ['f', 'm', 'female', 'male']:
                    raise ValueError
                actor.gender = request_body.get('gender')

            actor.update()

        except ValueError as e:
            abort(422)

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'actor': actor.format()
        })

    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actors(payload, id):
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

        except Exception:
            abort(500)

        return jsonify({
            'success': True,
            'actor_id': id
        })

    # Error Handlers

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': "Resource not found"
        }), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'An error has occurred, please try again'
        }), 500

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Unprocessable entity'
        }), 422

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            'success': False,
            'error': 401,
            'message': 'Unauthorized'
        }), 401

    @app.errorhandler(AuthError)
    def process_AuthError(error):
        response = jsonify(error.error)
        response.status_code = error.status_code
        return response

    return app


app = create_app()
'''
if __name__ == '__main__':
    APP.run(port=8080, debug=True)'''

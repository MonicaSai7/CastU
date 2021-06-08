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

    # Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    CORS(app, resources={'/': {'origins': '*'}})

    db_drop_and_create_all()

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
    def get_all_movies():
        movies_query = Movie.query.order_by(Movie.id).all()
        return jsonify({
            'success': True,
            'movies': [movie for movie in movies_query]
        }), 200

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_movie():
        try:
            request_body = request.get_json()
            if 'title' not in request_body \
                or 'release_date' not in request_body \
                or 'cast' not in request_body:
                abort(422)
            
            new_movie = Movie(
                request_body.get('title'),
                request_body.get('release_date'),
                request_body.get('cast')
            )

            actors = Actor.query.filter_by(Actor.name.in_(request_body.get('cast'))).all()

            if len(request_body.get('cast')) == len(actors):
                new_movie.cast = actors
                new_movie.insert()
            else:
                abort(422)
        
        except Exception:
            abort(422)
        
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
            if 'title' not in request_body \
                or 'release_date' not in request_body:
                abort(422)
            
            movie.title = request_body.get('title')
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
            'movie_id': movie.id
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
    
    


            

    return app

APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
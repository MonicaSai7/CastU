import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from database.models import setup_db, Actor, Movie


class CastUTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.user_token = os.environ['user_token']
        self.manager_token = os.environ['manager_token']
        self.admin_token = os.environ['admin_token']
        self.app = create_app()
        self.client = self.app.test_client
        setup_db(self.app)

        self.VALID_NEW_ACTOR = {
            "name": "Emma Stone",
            "age": 32,
            "gender": "F"
        }

        self.INVALID_NEW_ACTOR = {
            "name": "Emma Stone"
        }

        self.VALID_UPDATE_ACTOR = {
            "name": "Anne Hathaway"
        }

        self.INVALID_UPDATE_ACTOR = {}

        self.VALID_NEW_MOVIE = {
            "title": "Cruella",
            "release_data": "22-05-2021",
            "cast": ["Emma Stone"]
        }

        self.INVALID_NEW_MOVIE = {
            "title": "Cruella",
            "cast": ["Emma Stone"]
        }

        self.VALID_UPDATE_MOVIE = {
            "title": "Disney Cruella"
        }

        self.INVALID_UPDATE_MOVIE = {}

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_health(self):
        """Test for GET / (health endpoint)"""
        res = self.client().get('/')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertIn('success', data)
        self.assertEqual(data['success'], True)

    def test_api_call_without_token(self):
        """Failing Test trying to make a call without token"""
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertEqual(data["message"], "Authorization Header is required.")

    def test_get_actors(self):
        """Passing Test for GET /actors"""
        res = self.client().get('/actors', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('actors', data)
        self.assertTrue(len(data["actors"]))

    def test_get_actors_by_id(self):
        """Passing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertIn('name', data['actor'])
        self.assertTrue(len(data["actor"]["movies"]))

    def test_404_get_actors_by_id(self):
        """Failing Test for GET /actors/<actor_id>"""
        res = self.client().get('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_actor_with_user_token(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_actor(self):
        """Passing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('actor_id', data)

    def test_422_create_actor(self):
        """Failing Test for POST /actors"""
        res = self.client().post('/actors', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_NEW_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_actor_info(self):
        """Passing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor', data)
        self.assertEqual(data["actor"]["name"],
                         self.VALID_UPDATE_ACTOR["name"])

    def test_422_update_actor_info(self):
        """Failing Test for PATCH /actors/<actor_id>"""
        res = self.client().patch('/actors/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_UPDATE_ACTOR)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_actor_with_manager_token(self):
        """Failing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/5', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/5', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('actor_id', data)

    def test_404_delete_actor(self):
        """Passing Test for DELETE /actors/<actor_id>"""
        res = self.client().delete('/actors/100', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_get_movies(self):
        """Passing Test for GET /movies"""
        res = self.client().get('/movies', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
        self.assertTrue(data["success"])
        self.assertIn('movies', data)
        self.assertTrue(len(data["movies"]))

    def test_get_movie_by_id(self):
        """Passing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertIn('title', data['movie'])
        self.assertIn('release_date', data['movie'])
        self.assertIn('cast', data['movie'])
        self.assertTrue(len(data["movie"]["cast"]))

    def test_404_get_movie_by_id(self):
        """Failing Test for GET /movies/<movie_id>"""
        res = self.client().get('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_create_movie_with_user_token(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.user_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_create_movie(self):
        """Passing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 201)
        self.assertTrue(data["success"])
        self.assertIn('movie_id', data)

    def test_422_create_movie(self):
        """Failing Test for POST /movies"""
        res = self.client().post('/movies', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_NEW_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_update_movie_info(self):
        """Passing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.VALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie', data)
        self.assertEqual(data["movie"]["title"],
                         self.VALID_UPDATE_MOVIE["title"])

    def test_422_update_movie_info(self):
        """Failing Test for PATCH /movies/<movie_id>"""
        res = self.client().patch('/movies/1', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        }, json=self.INVALID_UPDATE_MOVIE)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertFalse(data['success'])
        self.assertIn('message', data)

    def test_delete_movie_with_manager_token(self):
        """Failing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.manager_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertFalse(data["success"])
        self.assertIn('message', data)

    def test_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/3', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["success"])
        self.assertIn('movie_id', data)

    def test_404_delete_movie(self):
        """Passing Test for DELETE /movies/<movie_id>"""
        res = self.client().delete('/movies/100', headers={
            'Authorization': "Bearer {}".format(self.admin_token)
        })
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('message', data)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
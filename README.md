# CastU
The CastU models a company that is responsible for creating movies and managing and assigning actors to those movies. This application allows the film crew to easily maintain a shared database with casting decisions stored with proper data integrity.

The motivation behind this project is to reinforce the skills acquired throughout thw Full Stack Web Developer Nanodegree at Udacity:
```
    - Coding in Python 3
    - Relational Database Architecture
    - Modeling Data Objects with SqlAlchemy
    - Internet Protocols and Communication
    - Developing a Flask API
    - Authentication and Access
    - Authentication with Auth0
    - Authentication in Flask
    - Role-Based Access Control (RBAC)
    - Testing Flask Applications
    - Deploying Applications
```

Access Heroku app at: https://castu-agency.herokuapp.com/

## Installations
It is recommended to set up the application in a Python virtual environment with Python 3.7.0<br>
For detailed instructions refer [Python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/).

After the virtual environment is set up and activated, install the dependencies by running:

```bash
pip install -r requirements.txt
```

##### Key Dependencies
- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) and [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) are libraries to handle the lightweight sqlite database. Since we want you to focus on auth, we handle the heavy lift for you in `./database/models.py`. We recommend skimming this code first so you know how to interface with the Drink model.

- [jose](https://python-jose.readthedocs.io/en/latest/) JavaScript Object Signing and Encryption for JWTs. Useful for encoding, decoding, and verifying JWTS.

## Running the server

From within the `.` directory first ensure you are working using your created virtual environment.<br>
Also, uncomment the line `db_drop_and_create_all()` on the initial run to setup the required tables in the database.
Each time you open a new terminal session, run:

```bash
export DATABASE_URL=<database-connection-url>
export FLASK_APP=app.py;
```

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.
## API Specifications
1. Models:
    - Movies with attributes title and release date
    - Actors with attributes name, age and gender

2. Endpoints:
    - GET /actors and /movies
    - DELETE /actors/ and /movies/
    - POST /actors and /movies and
    - PATCH /actors/ and /movies/

3. Roles:
    #### Casting Assistant
        - Can view actors and movies
            - get:actors
            - get:actors-details
            - get:movies
            - get:movies-details
    #### Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
            - post:actors
            - patch:actors
            - delete:actors
            - patch:movies
    #### Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database
            - post:movies
            - delete:movies

## Endpoints

#### GET /
 - General
   - check if the api is up and running
   - is a public endpoint, requires no authentication
 
 - Sample Request
   - `https://castu-agency.herokuapp.com`

<details>
<summary>Sample Response</summary>

```
{
    "success":true
}
```

</details>

#### GET /actors
 - General
   - gets the list of all the actors
   - requires `get:actors` permission
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors`

<details>
<summary>Sample Response</summary>

```
{
    "actors": [
        {
            "id": 1,
            "name": "Emma Stone"
        },
        {
            "id": 2,
            "name": "Robert Downey Jr."
        }
    ],
    "success": true
}
```

</details>

#### GET /actors/{actor_id}
 - General
   - gets the complete details of an actor
   - requires `get:actors-details` permission
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors/1`

<details>
<summary>Sample Response</summary>

```
{
    "actor": {
        "age": 32,
        "gender": "Female",
        "movies": [
            "Cruella"
        ],
        "name": "Emma Stone"
    },
    "success": true
}
```
  
</details>

#### POST /actors
 - General
   - creates a new actor
   - requires `post:actors` permission
 
 - Request Body
   - name: string, required
   - age: integer, required
   - gender: string, required
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors`
   - Request Body
     ```
        {
            "name": "Emma Stone",
            "age": 32,
            "gender": "Female"
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actor_id": 1,
    "success": true
}
```
  
</details>

#### PATCH /actors/{id}
 - General
   - updates the details of an actor
   - requires `patch:actors` permission
 
 - Request Body (at least one of the following fields required)
   - name: string, optional
   - age: integer, optional
   - gender: date, optional
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors/5`
   - Request Body
     ```
       {
            "age": 35
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "actor": {
        "age": 35,
        "gender": "Female",
        "name": "Emma Stone"
    },
    "success": true
}
```
  
</details>

#### DELETE /actors/{id}
 - General
   - deletes the actor
   - requires `delete:actors` permission
   - will also delete the mapping to the movie but will not delete the movie from the database
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors/1`

<details>
<summary>Sample Response</summary>

```
{
    "actor_id": 1,
    "success": true
}
```
  
</details>

#### GET /movies
 - General
   - gets the list of all the movies
   - requires `get:movies` permission
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/movies`

<details>
<summary>Sample Response</summary>

```
{
    "movies": [
        {
            "id": 1,
            "release_date": "21-05-2021",
            "title": "Cruella"
        },
        {
            "id": 2,
            "release_date": "01-05-2021",
            "title": "Conjuring 3"
        }
    ],
    "success": true
}
```

</details>

#### GET /movies/{id}
 - General
   - gets the complete info for a movie
   - requires `get:movies-details` permission
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "movie": {
        "cast": [
            "Emma Stone"
        ],
        "release_date": "01-05-2021",
        "title": "Cruella"
    },
    "success": true
}
```
  
</details>

#### POST /movies
 - General
   - creates a new movie
   - requires `post:movies` permission
 
 - Request Body
   - title: string, required
   - release_date: string, required
   - cast: array of string, non-empty, required
 
 - NOTE
   - Actors passed in the `cast` array in request body must already exist in the database prior to making this request.
   - If not, the request will fail with code 422.
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/actors`
   - Request Body
     ```
        {
            "title": "Cruella",
            "release_date": "01-05-2021",
            "cast": ["Emma Stone"]
        }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movie_id": 1,
    "success": true
}
```
  
</details>

#### PATCH /movie/{id}
 - General
   - updates the info for a movie
   - requires `patch:movies` permission
 
 - Request Body (at least one of the following fields required)
   - title: string, optional
   - release_date: integer, optional
   - cast: array of string, non-empty, optional
 
 - NOTE
   - Actors passed in the `cast` array in request body will completely replace the existing relationship.
   - So, if you want to append new actors to a movie, pass the existing actors also in the request.
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/movies/1`
   - Request Body
     ```
       {
            "title": "Disney Cruella"
       }
     ```

<details>
<summary>Sample Response</summary>

```
{
    "movie": {
        "release_date": "01-05-2021",
        "title": "Disney Cruella"
    },
    "success": true
}
```
  
</details>

#### DELETE /movies/{movie_id}
 - General
   - deletes the movie
   - requires `delete:movies` permission
   - will not affect the actors present in the database
 
 - Sample Request
   - `https://castu-agency.herokuapp.com/movies/1`

<details>
<summary>Sample Response</summary>

```
{
    "movie_id": 1,
    "success": true
}
```
  
</details>

## Error Handlers

The error codes currently returned are:

* 401 – Unauthorized
* 404 – Resource Not Found
* 422 – Unprocessable
* 500 – Internal Server Error

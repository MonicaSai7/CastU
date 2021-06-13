# CastU
The CastU models a company that is responsible for creating movies and managing and assigning actors to those movies.

Access Heroku app at: https://castu-agency.herokuapp.com/

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
    #### Casting Director
        - All permissions a Casting Assistant has and…
        - Add or delete an actor from the database
        - Modify actors or movies
    #### Executive Producer
        - All permissions a Casting Director has and…
        - Add or delete a movie from the database

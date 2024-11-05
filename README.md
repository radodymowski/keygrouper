# KeyGrouper v0.1.1

### About
This project implements functionality to group keys stored in a CSV file by the most descriptive prefixes 
and return them as a JSON-formatted object. It also serves a REST API for displaying, creating new groups,
and moving existing entities between groups.

### Installation
1. Download the project repository.
2. Run `docker compose up -d`
3. For prepopulating database with objects based on `names.csv`, run `docker compose run web python manage.py load_names --save`.
4. After the container is up, run `docker compose run web python manage.py createsuperuser` to create your local admin account.
5. Names from names.csv file should be automatically grouped and populated in the local database.

### Usage
#### Key grouping service
To check keys grouper demo based on the provided `names.csv` file, run `python manage.py load_names` - the command will
output JSON-formatted names grouped by prefixes.

#### REST API
After running the server, the following endpoints will be available:
- `http://0.0.0.0:8000/api/token/ POST` for obtaining JWT authentication token. 
Add it as Bearer token to Authorization headers for accessing the rest of the endpoints.
- `http://0.0.0.0:8000/names GET ` for listing folders containing grouped names.
- `http://0.0.0.0:8000/names POST` for creating a new folder.
- `http://0.0.0.0:8000/names/1/move PUT` for moving name entity to another folder.

For more information, please check `Documentation`.

### Documentation
Once the server is running, docs are available under `http://0.0.0.0:8000/docs/` page.

### Testing
If the container is already built, simply run `pytest` to run all unit tests.

### Concepts and follow-up questions
Some solutions implemented in this project are designed for demo purposes, to make it simpler. 
The default sqlite3 database engine is used, as it is sufficient for a small demo file and simple models. 
For large datasets, I could think about other solutions -
e.g. instead of local database, I would consider using some cloud-based database, e.g. AWS DynamoDB - as the database schema 
is simple, but for big amount of data this could be a better choice for performance solutions.

Another solution for speeding up performance of groups big amount of data is chunking the file and sending the grouping
as async task (possibly using asyncio). Alternative is implementing message queue - there we could go with Celery or some
cloud solutions, e.g. AWS SQS.

Talking about deploying this application to production, logging and monitoring tools should not be missed - 
I would recommend simple solutions like Sentry, as for small size of the project. 

Used 3rd party libraries:
- Django & Django REST Framework - for REST API implementation, chosen as preferred,
- pytest-django - extension for pytest for simple unit tests implementation,
- djangorestframework-simplejwt - extension for quick implementation of JWT token authorization,
- drf-spectacular - for quick generation of automated docs.
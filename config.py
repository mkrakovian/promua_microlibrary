import os

BASE_DIR = os.path.dirname(__file__)

DATABASE_NAME = 'microlib.db'

SEARCHBASE_NAME = 'search'

WHOOSH_BASE = os.path.join(BASE_DIR, SEARCHBASE_NAME)

SQLALCHEMY_DATABASE_URI = ''.join(['sqlite:///', os.path.join(BASE_DIR, DATABASE_NAME)])

CSRF_ENABLED = True

SECRET_KEY = 'you-will-never-guess-one'
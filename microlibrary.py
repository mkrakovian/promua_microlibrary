from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask_wtf.csrf import CsrfProtect
from config import BASE_DIR, DATABASE_NAME
from flask_bootstrap import Bootstrap
import os

app = Flask(__name__)
app.config.from_object('config')
CsrfProtect(app)
lm = LoginManager(app)
lm.login_view = 'login'
Bootstrap(app)
db = SQLAlchemy(app)


from views import *
import models


if __name__ == '__main__':

    # Checking if our db exists, creating and supplying initial data if it doesn't.
    # NOTE: this will work fine only for SQLite engine (the db file is saved on disk).
    if not os.path.exists(os.path.join(BASE_DIR, DATABASE_NAME)):
        from database import db_init
        db_init()
    app.run(debug=True)
from microlibrary import db, app
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.whooshalchemy import whoosh_index


class User(db.Model):
    __tablename__ = "users"
    id = db.Column('user_id', db.Integer, primary_key=True)
    username = db.Column('username', db.String(20), unique=True, index=True)
    pw_hash = db.Column('password', db.String(70))

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.pw_hash, password)

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.id)

    def __unicode__(self):
        return self.username


assoc = db.Table(
    'association',
    db.Column('book_id', db.Integer, db.ForeignKey('books.id')),
    db.Column('author_id', db.Integer, db.ForeignKey('authors.id')),

)


class Book(db.Model):
    __tablename__ = 'books'
    __searchable__ = ['title']
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text(100), unique=True)
    authors = db.relationship('Author', secondary=assoc,
                              backref=db.backref('books', lazy='dynamic'), lazy='dynamic')

    def __unicode__(self):
        return self.title

    def __repr__(self):
        return '<Book: %s>' % self.title


class Author(db.Model):
    __tablename__ = 'authors'
    __searchable__ = ['name']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text(50), unique=True)

    def __unicode__(self):
        return self.name

    def __repr__(self):
        return '<Author: %s>' % self.name


def get_all_authors():
    return Author.query.all()

whoosh_index(app, Book)
whoosh_index(app, Author)
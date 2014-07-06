from models import *


def db_init():
    """
    Creating all the necessary tables. Supplying initial data.
    """
    author1 = Author(name='Wesley J. Chun')
    author2 = Author(name='Jeff Forcier')
    author3 = Author(name='Paul Bissex')
    author4 = Author(name='Allen W. Dulles')
    book1 = Book(title="Core python programming", authors=[author1])
    book2 = Book(title="Python Web Development with Django", authors=[author1, author2, author3])
    book3 = Book(title="The Craft of Intelligence", authors=[author4])
    db.create_all()
    db.session.add_all([author1, author2, author3, author4, book1, book2, book3])
    db.session.commit()
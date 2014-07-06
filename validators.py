from microlibrary import db
from models import Book, Author


def author_exists_create(form):
    """
    Checks if the proposed author already exists in the db.
    form : form object, represents the proposed author's data.
    """
    author = Author.query.filter_by(name=form.name.data).first()
    if author:
        form.errors.update({'name': ["This author is already present in our list."]})
    return author


def book_exists_create(form):
    """
    Checks if the proposed book already exists in the db (title uniqueness is enforced by WhooshAlchemy).
    form: form object, represents the proposed book's data.
    """
    book = Book.query.filter_by(title=form.title.data).first()
    if book:
        form.errors.update({'title': ["Book with this title is already in our list"]})
    return book


def author_exists_edit(prev_name, form):
    """
    Checks if the edited author already exists in the db.
    form : form object, represents the edited author's data.
    prev_name: str, represents the author's name before editing.
    """
    if prev_name == form.name.data:
        return False
    else:
        author = Author.query.filter_by(name=form.name.data).first()
        if author:
            form.errors.update({'name': ["This author is already present in our list."]})
        return author


def book_exists_edit(prev_title, form):
    """
    Checks if the edited book already exists in the db.
    form: form object, represents the edited book's data.
    prev_title: str, represents the book's title before editing.
    """
    if prev_title == form.title.data:
        return False
    else:
        book = Book.query.filter_by(title=form.title.data).first()
        if book:
            form.errors.update({'title': ["Book with this title is already in our list"]})
        return book
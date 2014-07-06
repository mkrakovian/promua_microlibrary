from microlibrary import app, db, lm
from flask import render_template, flash, redirect
from flask import request
from forms import AddBookForm, AddAuthorForm, LibraryLoginForm, LibraryRegisterForm
from models import Book, Author, User
from flask.helpers import url_for
from validators import author_exists_create, book_exists_create, book_exists_edit, author_exists_edit
from flask.ext.login import login_user, logout_user, login_required
import string


@app.route('/library')
def library():
    books = Book.query.limit(10).all()
    return render_template('library_index.html',
                           books=books)


@app.route('/library/add_book', methods=['GET', 'POST'])
@login_required
def library_add_book():
    form = AddBookForm()
    if form.validate_on_submit() and not book_exists_create(form):
        new_book = Book(title=form.title.data, authors=form.authors.data)
        db.session.add(new_book)
        db.session.commit()
        flash("U have successfully added a new book, titled '%s'." % form.title.data)
        return redirect(url_for('library'))
    return render_template('library_add_book.html',
                           form=form)


@app.route('/library/add_author', methods=['GET', 'POST'])
@login_required
def library_add_author():
    form = AddAuthorForm()
    if form.validate_on_submit() and not author_exists_create(form):
        new_author = Author(name=form.name.data)
        db.session.add(new_author)
        db.session.commit()
        flash("U have successfully added a new author '%s'" % form.name.data)
        if request.args.get('book_id'):
            return redirect(url_for('library_edit_book', book_id=request.args.get('book_id')))
        return redirect(url_for('library_add_book'))
    return render_template('library_add_author.html',
                           form=form)


@app.route('/library/book/<int:book_id>', methods=['GET', 'POST'])
@login_required
def library_edit_book(book_id):
    book = Book.query.get_or_404(book_id)
    form = AddBookForm(obj=book)
    if form.validate_on_submit() and not book_exists_edit(book.title, form):
        book.title = form.title.data
        book.authors = form.authors.data
        db.session.commit()
        flash("U have successfully edited the book, titled '%s'" % form.title.data)
        return redirect(url_for('library'))
    return render_template('library_edit_book.html',
                           form=form)


@app.route('/library/authors')
def library_authors():
    authors = Author.query.all()
    return render_template('library_authors.html',
                           authors=authors)


@app.route('/library/author/<int:author_id>', methods=['GET', 'POST'])
@login_required
def library_edit_author(author_id):
    author = Author.query.get_or_404(author_id)
    form = AddAuthorForm(obj=author)
    if form.validate_on_submit() and not author_exists_edit(author.name, form):
        author.name = form.name.data
        db.session.commit()
        flash("U have successfully edited '%s'" % form.name.data)
        if not request.args.get('book_id'):
            return redirect(url_for('library'))
        return redirect(url_for('library_edit_book', book_id=request.args.get('book_id')))
    return render_template('library_edit_author.html',
                           form=form)


@app.route('/library/book/delete/<int:book_id>', methods=['GET', 'POST'])
@login_required
def library_delete_book(book_id):
    book = Book.query.get_or_404(book_id)
    book_authors = book.authors.all()
    book_title = book.title
    if request.method == 'POST':
        db.session.delete(book)
        db.session.commit()
        flash("U have successfully deleted the book, titled '%s'" % book_title)

        # If authors of the deleted book have no other books in our MicroLibrary, then they should be deleted as well
        for author in book_authors:
            if not author.books.all():
                author_name = author.name
                db.session.delete(author)
                db.session.commit()
                flash("'%s' has no more books in our library and was successfully deleted." % author_name)
        return redirect(url_for('library'))
    return render_template('library_delete_book.html', title=book_title)


@app.route('/library/author/delete/<int:author_id>', methods=['GET', 'POST'])
@login_required
def library_delete_author(author_id):
    author = Author.query.get_or_404(author_id)
    author_name = author.name
    if request.method == 'POST':
        db.session.delete(author)
        db.session.commit()
        flash("U have successfully deleted '%s'" % author_name)
        return redirect(url_for('library_authors'))
    return render_template('library_delete_author.html', name=author_name)


@app.route('/library/search', methods=['POST'])
def library_search():
    if not request.form.get('search_query'):
        flash("Please provide the search query.")
    else:
        search_query = request.form.get('search_query')
        # First, let's strip our sq off punctuation signs and limit it to 10 words.
        valid_sq = " ".join([elem.strip(string.punctuation) for elem in search_query.split(' ')[:10]]).strip(' ')

        # Now search for our sq in books and authors (cause it may be either). Search with AND & OR conjunctions.
        book_search_and = Book.query.whoosh_search(valid_sq).all()
        book_search_or = Book.query.whoosh_search(valid_sq, or_=True).all()
        author_search_and = Author.query.whoosh_search(valid_sq).all()
        author_search_or = Author.query.whoosh_search(valid_sq, or_=True).all()

        # Now combine the results of AND/OR searches.
        # Note: the order matters, results are ranked by relevance in Whoosh.
        books, authors = [], []

        books.extend(book_search_and)
        for book in book_search_or:
            if book not in books:
                books.append(book)

        authors.extend(author_search_and)
        for author in author_search_or:
            if author not in authors:
                authors.append(author)
        return render_template('library_search.html',
                               books=books, authors=authors, sq=search_query)
    return render_template('library_search.html')


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/library/register', methods=['GET', 'POST'])
def library_register():
    form = LibraryRegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.pass_reenter.data:
            form.errors.update({'pass_reenter': ["Entered passwords didn't match."]})
        else:
            user = User(username=form.username.data, password=form.password.data)
            db.session.add(user)
            db.session.commit()
            flash("New user successfully added.")
            return redirect(url_for('login'))
    return render_template('library_register.html', form=form)


@app.route('/library/login', methods=['GET', 'POST'])
def login():
    form = LibraryLoginForm()
    error = ''
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not (user and user.check_password(form.password.data)):
            error = "Incorrect username & password."
        else:
            login_user(user, remember=form.remember_me.data)
            flash("U were successfully logged in.")
            return redirect(request.args.get('next') or url_for('library'))
    return render_template('library_login.html', form=form, error=error)


@app.route('/library/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('library'))
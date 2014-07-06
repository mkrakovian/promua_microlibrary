from flask.ext.wtf import Form
from wtforms import StringField, BooleanField, HiddenField, PasswordField
from wtforms.ext.sqlalchemy.fields import QuerySelectMultipleField
from wtforms.validators import DataRequired, Length, ValidationError
from models import get_all_authors, User


class AddBookForm(Form):
    id = HiddenField("book's id")
    title = StringField("book's title", validators=[DataRequired()])
    authors = QuerySelectMultipleField("book's authors", query_factory=get_all_authors, validators=[DataRequired()])


class AddAuthorForm(Form):
    name = StringField("author's name", validators=[DataRequired()])


class LibraryLoginForm(Form):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)


class LibraryRegisterForm(Form):

    username = StringField('username', validators=[DataRequired(),
                                                   Length(min=3, max=20,
                                                          message="Ur username should be 3 to 20 characters long.")])
    password = PasswordField('password', validators=[DataRequired(),
                                                     Length(min=5,
                                                            message="Ur pass should be at least 5 characters long.")])
    pass_reenter = PasswordField('password', validators=[DataRequired()])

    def validate_username(form, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError("Try to choose a different username.")

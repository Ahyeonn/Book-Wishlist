# Create your models here.
from sqlalchemy_utils import URLType

from book_app.extensions import db
from book_app.utils import FormEnum
from flask_login import UserMixin
from enum import unique

class BookGenre(FormEnum):
    """Categories of book genres."""
    FANTASY = 'Fantasy'
    YOUNGADULT = 'Young Adult'
    CHILDREN = 'Children'
    ROMANCE = 'Romance'
    HISTORICAL = 'Historical'
    THRILLER = 'Thriller'
    FICTION = 'Fiction'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    readcompletes = db.relationship(
        'ReadCompleted', secondary='completed_list', back_populates='users')
    wishtoreads = db.relationship(
        'WishToRead', secondary='wishlist_list', back_populates='users')

class WishToRead(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType)
    category = db.Column(db.Enum(BookGenre), default=BookGenre.FICTION)
    description = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users = db.relationship(
        'User', secondary='wishlist_list', back_populates='wishtoreads')

class ReadCompleted(db.Model):
    """Grocery Store model."""
    id = db.Column(db.Integer, primary_key=True)
    book_name = db.Column(db.String(80), nullable=False)
    photo_url = db.Column(URLType)
    category = db.Column(db.Enum(BookGenre), default=BookGenre.FICTION)
    description = db.Column(db.String(200), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_by = db.relationship('User')
    users = db.relationship(
        'User', secondary='completed_list', back_populates='readcompletes')

user_completed_table = db.Table('completed_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('completed_id', db.Integer, db.ForeignKey('read_completed.id'))
)

user_wishlist_table = db.Table('wishlist_list',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('wishtoread_id', db.Integer, db.ForeignKey('wish_to_read.id'))
)
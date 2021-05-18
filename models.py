# --------------------------------------------------------------
# Name:     models
# Purpose:  To store the user model to be used in the app. Note:
#           this file contains multiple classes because certain
#           classes depend on the User model, and at the same
#           time the user model depends on those classes. Placing
#           these classes in individual files results in a cyclic
#           import that breaks the code.
#
# References: This program uses Flask libraries Bcrypt and Login
#                   as well as the database creator Peewee.
#
# Author:     Neil Mehta
# Created:    13-Mar-2019
# Updated:    12-Jun-2019
# --------------------------------------------------------------

import datetime

from flask_bcrypt import generate_password_hash

from flask_login import UserMixin

from peewee import *


DATABASE = SqliteDatabase('public.db')


class User(UserMixin, Model):
    '''
    A user object that holds the username, email, password,
    join date, and admin privileges of said user.

    Attributes
    ----------
    username  : str
                Username of user defined as a "character field"
                in Flask. Must be unique.
    email     : str
                User's email. Defined as a character field.
                Must be unique.
    password  : str
                User's password. Defined as a character field.
                Must be unique.
    joined_at : basic field
                Stores the date at which the user joined and
                organizes posts according to that join date.
    is_admin  : bool
                Determines whether user has admin privileges
                or not. Default is set to false.

    Methods  (Change to an __init__())
    -------
    create_user() -> None
            Uses the database created in the 'postform.py' file
            to store the user's information and create their
            account.

    '''
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)
    is_admin = BooleanField(default=False)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at',)

    def get_posts(self):
        return Post.select().where(Post.user == self)

    def get_stream(self):
        return Post.select().where(
            (Post.user << self.following) |
            (Post.user == self)
        )

    @property
    def following(self):
        return (
            User.select().join(
                Relationship, on=Relationship.to_user
            ).where(
                Relationship.from_user == self
            )
        )

    @property
    def followers(self):
        return (
            User.select().join(
                Relationship, on=Relationship.from_user
            ).where(
                Relationship.to_user == self
            )
        )

    '''The @classmethod allows us to call the method using class name 
    instead of object'''

    @classmethod
    def create_user(cls, username, email, password, admin=False):
        '''
        Creates user's account by storing information in database.


        Parameters
        ----------
        username  : str
                    User's desired username. Must be unique.
        email    : str
                   User's associated email. Must be unique.
        password : str
                   Password associated with user's account.
        admin    : bool
                   Determines whether user has admin privileges.


        Returns
        -------
        Model
                Creates user's account based on the model.


        Raises
        ------
        ValueError
            If the username or email are already in use by an account.

        '''
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                    is_admin=admin)
        except IntegrityError:
            raise ValueError("User already exists")


class Relationship(Model):
    '''
        A relationship object that displays the relationship between
        multiple users (ie. followers, following).

        Attributes
        ----------
        from_user : str
                    Displays how many people follow said user.
        to_user   : str
                    Displays how many people said user is following.

        Methods
        -------
        The class has no methods as it's job is to store information
        about follower accounts and accounts being followed by a user.
        Instead, it has a sublcass "Meta" to provide metadata (atttributes)
        to corresponding fields in the SQLite database.
    '''
    from_user = ForeignKeyField(User, backref='relationships')
    to_user = ForeignKeyField(User, backref='related_to')

    class Meta:
        database = DATABASE
        indexes = (
            (('from_user', 'to_user'), True),
        )


class Post(Model):
    '''
        A post object that holds the string of characters posted
        by a user. Contains a timestamp of the post, the username
        of the user, and the content (string) posted.

        Attributes
        ----------
        timestamp : basic field
                    Timestamp of when post was created.
        usern      : str
                    Which user created the post. Used as a
                    ForeignKeyField.
        content   : str
                    The actual writing in the post.

        Methods
        -------
        The class has no methods as it's job is to store information
        about what the user wants to post. Instead, it has a sublcass
        "Meta" to provide metadata (attributes) to corresponding fields
        in the SQLite database.

        '''
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(
        User, backref='posts'
    )
    content = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Post, Relationship], safe=True)
    DATABASE.close()

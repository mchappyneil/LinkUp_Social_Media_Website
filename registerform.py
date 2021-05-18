# --------------------------------------------------------------
# Name:     registerform
# Purpose:  Allows user to register with inputted information
#
# References: This program uses the Flask library WTF and the
#             library WTForms. WTForms is extended to obtain
#             validators. Documentation for WTForms used from
#             https://wtforms.readthedocs.io/en/stable/fields.html
#
# Author:     Neil Mehta
# Created:    23-Mar-2019
# Updated:    12-Jun-2019
# --------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)

from models import User


def name_exists(form, field):
    '''
            Checks whether username is valid or not.


            Parameters
            ----------
            form  : form (documentation from WTForms website)
                    The form which the field belongs to.

            field : field
                    Field created by the form.


            Returns
            -------
            Void
                Accepts the username inputted as valid

            Raises
            ------
            ValueError
                If the username is already in use by an account.

            '''
    if User.select().where(User.username == field.data).exists():
        raise ValidationError('User with that name already exists.')


def email_exists(form, field):
    '''
            Checks whether email is valid or not.


            Parameters
            ----------
            form  : form
                    The form which the field belongs to.

            field : field
                    Field created by the form.


            Returns
            -------
            void
                Accepts the email inputted as valid

            Raises
            ------
            ValueError
                If the email is already in use by an account.

            '''
    if User.select().where(User.email == field.data).exists():
        raise ValidationError('User with that email already exists.')


class RegisterForm(FlaskForm):
    '''
    A registration object that receives and records the username, email,
    and password of a user. Also uses 'password2' to validate the
    password and make sure they match.

    Attributes
    ----------
    username   : str
                Username of user defined as a "character field"
                in Flask. Must be unique.
    email      : str
                User's email. Defined as a character field.
                Must be unique.
    password   : str
                User's password. Defined as a character field.
                Must be the same as password2.
    password2 : str
                Repetition of user's password. Must match
                password.


    Methods
    -------
    The class is used as an Entity, for data transfer and so has no methods.

    '''
    username = StringField(
        'Username',
        validators=[
            DataRequired(),
            Regexp(
                r'^[a-zA-Z0-9_]+$',
                message="Username should be one word, letters, numbers, and underscores only."
            ),
            name_exists
        ])

    email = StringField(
        'Email',
        validators=[
            DataRequired(),
            Email(),
            email_exists
        ])

    password = PasswordField(
        'Password',
        validators=[
            DataRequired(),
            Length(min=2),
            EqualTo('password2', message='Passwords must match')
        ])

    password2 = PasswordField(
        'Confirm password',
        validators=[DataRequired()]
    )

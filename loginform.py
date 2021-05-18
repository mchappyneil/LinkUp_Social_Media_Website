# --------------------------------------------------------------
# Name:     loginform
# Purpose:  Allows users who already have accounts to log in.
#
# References: This program uses the Flask library WTF and the
#             library WTForms. WTForms is extended to obtain
#             validators. Documentation for WTForms used from
#             https://wtforms.readthedocs.io/en/stable/fields.html
#
# Author:     Neil Mehta
# Created:    13-Mar-2019
# Updated:    12-Jun-2019
# --------------------------------------------------------------

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import (DataRequired, Email)


class LoginForm(FlaskForm):
    '''
        A log-in object that receives the user's email and password.
        Unlike the registration form, since the user already signed
        up with an account, no username needs to be created and the
        password only needs to be inputted once. Requires some data
        to be inputted in order to sign in successfully (hence the
        validators DataRequired() and Email())

        Attributes
        ----------
        email    : str
                   User's email. Defined as a string field.
        password : str
                   User's password. Defined as a password field.


        Methods
        -------
        The class is used as an Entity for data transfer, and so has no methods.

        '''
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])

# --------------------------------------------------------------
# Name:     postform
# Purpose:  Allows users who have their own account and are
#           logged in to post messages to the stream. A form for
#           the post, if you will.
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
from wtforms import TextAreaField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    '''
        An object that allows users to post messages to their stream.
        Requires data to be inputted to post successfully.

        Attributes
        ----------
        content : str
                  The message the user wants to post.

        Methods
        -------
        This class is used as a Data Transfer Object (DTO), meant for communicating
        user inputs to the network and therefore has no methods.

    '''
    content = TextAreaField("Enter message", validators=[DataRequired()])

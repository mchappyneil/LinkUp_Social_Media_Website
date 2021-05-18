# --------------------------------------------------------------
# Name:     app
# Purpose:  To run the main program
#
# References: This program uses Flask, Flask-Bcrypt and
#             Flask-Login
#
# Author:     Neil Mehta
# Created:    13-Mar-2019
# Updated:    12-Jun-2019
# --------------------------------------------------------------

from flask import (Flask, g, render_template, flash, redirect, url_for, abort)
from flask_bcrypt import check_password_hash
from flask_login import (LoginManager, login_user, logout_user,
                         login_required, current_user)

import registerform
import loginform
import postform
import models

DEBUG = True
PORT = 8080
HOST = '127.0.0.1'

app = Flask(__name__)
app.secret_key = 'adsfhreqwdaf.34234lkhalradfopoiuqtadfadtrtgjhor!'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(userid):
    '''
    Function to load the current user's model from the
    database.

    Parameters
    ----------
    userid : Model
            The model of the current user to be loaded

    Returns
    -------
    Model
           Returns user model from the userid model

    Raises
    ------
    DoesNotExist
            If their account does not exist
    '''
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


@app.before_request
def before_request():
    '''
    Connect to the database before each request.

    Parameters
    ----------
    None

    Returns
    -------
    Model
           Connects and loads user model

    '''
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    '''
    Close the database after each request.

    Parameters
    ----------
    response : Hook
            Requires a request to activate response


    Returns
    -------
    Hook
           Returns the corresponding response to the
           request and closes the database


    '''
    g.db.close()
    return response


@app.route('/register', methods=('GET', 'POST'))
def register():
    '''
    Route to register for the social network

    Parameters
    ----------
    None

    Returns
    -------
    Form
                Registration form to fill out
    html template
                Visuals for the register page written in html

    '''
    form = registerform.RegisterForm()
    if form.validate_on_submit():
        flash("You registered successfully.", "success")
        models.User.create_user(
            username=form.username.data,
            email=form.email.data,
            password=form.password.data
        )
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


@app.route('/login', methods=('GET', 'POST'))
def login():
    '''
    Route to register for social network
    (only if user already has account)

    Parameters
    ----------
    None

    Returns
    -------
    Form
                Login form to fill out
    html template
                Login screen's visuals written in html
    flash message
                Flashes message if login was successful or unsuccessful
    redirect
                If login was successful user is redirected to home page

    Raises
    ------
    DoesNotExist
            If user's email or password is incorrect

    '''
    form = loginform.LoginForm()
    if form.validate_on_submit():
        try:
            identification = models.User.get(
                models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password does not match.", "error")
        else:
            if check_password_hash(identification.password, form.password.data):
                login_user(identification)
                flash("Login successful!", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password does not match.", "error")
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    '''
    Function to log user out of account

    Parameters
    ----------
    None

    Returns
    -------
    flash message
                Displays flash message to inform user of successful logout
    redirect
            Redirects user to index page

    '''
    logout_user()
    flash("Logout successful", "success")
    return redirect(url_for('index'))


@app.route('/new_post', methods=('GET', 'POST'))
@login_required
def post():
    '''
        Route to post on social network
        (only if user already has account)

        Parameters
        ----------
        None

        Returns
        -------
        Form
            Post form to fill out

        html template
            "Post" screen's visuals written in html

        '''
    form = postform.PostForm()
    if form.validate_on_submit():
        models.Post.create(user=g.user._get_current_object(),
                           content=form.content.data.strip())
        flash("Message posted successfully", "success")
        return redirect(url_for('index'))
    return render_template('post.html', form=form)


@app.route('/')
def index():
    '''
    The "main page" of the program

    Parameters
    ----------
    None

    Returns
    -------
    html template
                Main page's visuals written in html

    '''
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream=stream)


@app.route('/stream')
@app.route('/stream/<username>')
def stream(username=None):
    '''
    Function for the user's stream, where all posts are visible.

    Parameters
    ----------
    username : string
               Name of user displayed on screen

    Returns
    -------
    html template
                Visual file for user's stream page

    '''

    template = 'stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(
                models.User.username ** username).get()
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)


@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 0:
        abort(404)
    return render_template('stream.html', stream=posts)


@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username ** username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user=g.user._get_current_object(),
                to_user=to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash("Now following {}".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username ** username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user=g.user._get_current_object(),
                to_user=to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("No longer following {}".format(to_user.username), "success")
    return redirect(url_for('stream', username=to_user.username))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    try:
        models.initialize()
        models.User.create_user(
            username='testuser',
            email='test@example.com',
            password='password',
            admin=True
        )
    except ValueError:
        pass

    app.run(debug=DEBUG, host=HOST, port=PORT)

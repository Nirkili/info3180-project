"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from . import app, db, bcrypt
from flask import render_template, request, jsonify, send_file, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from .models import *
from .forms import *
import os


###
# Routing for your application.
###

@app.route('/')
def index():
    return redirect(url_for('login'))


# Auth Routes
@app.route('/api/v1/auth/register', methods = ['POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():

        # Get form Data
        first_name = form.first_name.data
        last_name = form.last_name.data
        username = form.username.data
        email = form.email.data
        dob = form.date_of_birth.data
        password = form.password.data
        gender = form.gender.data
        gender_preference = form.gender_preference.data
        relationship_preference = form.relationship_preference.data
        wants_children = form.wants_children.data





        # Ensure that there are no duplicate usernames
        if User.query.filter_by(user_name = username).first():
            return jsonify({'errors': [
                {'field': 'Username',
                 'message': 'Username not available'}
            ]}), 409

        # Ensure that there are no duplicate emails
        if User.query.filter_by(user_name = username).first():
            return jsonify({'errors': [
                {'field': 'Email',
                 'message': 'Email already registered'}
            ]}), 409
        
        # Hash password
        password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

        # Add User to the DB
        new_user = User(
            first_name = first_name,
            last_name = last_name,
            user_name = username,
            email = email,
            password = password_hash
        )

        db.session.add(new_user)
        db.session.flush() # Get new user ID

        # Create User profile
        new_profile = Profile(
            user_ID = new_user.user_ID,
            date_of_birth = dob,
            gender = gender,
            gender_preference = gender_preference,
            relationship_type_preference = relationship_preference,
            wants_children = wants_children,
            location = '',
            visibility_status = 'Public',
            picture_filename = ''

        )

        db.session.add(new_profile)
        db.session.commit()

        login_user(new_user)

        return jsonify({
            'message': 'Registration successful',
            'user_id': new_user.user_ID
        }), 201

    return jsonify({'errors': form_errors(form)}), 400



@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        # Get form data
        email = form.email.data
        password = form.password.data

        # Query the database
        user = User.query.filter_by(email = email).first()

        # Check if the user exists
        if user:
            if bcrypt.check_password_hash(user.password, password):
                login_user(user)
                
                return jsonify({
                    'message': 'Login Successful',
                    'user_id': user.user_ID
                }), 200
            
            return jsonify({'errors': [
            {'field': 'Credentials', 'message': 'Invalid email or password'}
        ]}), 401

    return jsonify({'errors': form_errors(form)}), 400
        

@app.route('/api/v1/auth/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out successfully'}), 200


# This function is for Vue. 
# When a user refreshes a page Vue's memory is wiped, so it needs to check flask session cookies
@app.route('/api/v1/auth/status', methods=['GET'])
def auth_status():
    if current_user.is_authenticated:
        return jsonify({'logged_in': True, 'user_id': current_user.user_ID}), 200
    return jsonify({'logged_in': False}), 200



# Profile Routes
@app.route('/api/v1/profile', methods=['GET'])
@login_required
def get_my_profile():
    pass

@app.route('/api/v1/profile', methods=['POST'])
@login_required
def update_profile():
    pass

@app.route('/api/v1/profile/<int:user_id>', methods=['GET'])
@login_required
def get_profile(user_id):
    pass

@app.route('/api/v1/profile/interest', methods = ['POST'])
@login_required
def interest():
    pass

# CSRF
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

###
# The functions below should be applicable to all Flask apps.
###


def logout_user():
    pass


# Here we define a function to collect form errors from Flask-WTF
def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
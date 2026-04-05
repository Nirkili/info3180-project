"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, redirect, url_for
import os
from .models import User 


###
# Routing for your application.
###

@app.route('/')
def index():
    return redirect(url_for('login'))


# Auth Routes

@app.route('/api/v1/auth/register', methods = ['POST'])
def register():
    pass

@app.route('/api/v1/auth/login', methods = ['POST'])
def login():
    pass

@app.route('/api/v1/auth/interest', methods = ['POST'])
def interest():
    pass

@app.route('/api/v1/auth/logout')
def logout():
    pass

@app.route('/api/v1/auth/status', methods=['GET'])
def auth_status():
    pass


# Profile Routes
@app.route('/api/v1/profile', methods=['GET'])
def get_my_profile():
    pass

@app.route('/api/v1/profile', methods=['POST'])
def update_profile():
    pass

@app.route('/api/v1/profile/<int:user_id>', methods=['GET'])
def get_profile(user_id):
    pass


# CSRF

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
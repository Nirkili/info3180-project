"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from . import app, db, bcrypt
from flask import render_template, request, jsonify, send_file, redirect, url_for, send_from_directory
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from .models import *
from .forms import *
from .matching_algorithm import calc_score
import os


###
# Routing for your application.
###

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
        if User.query.filter_by(email = email).first(): #fix
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

        login_user(new_user) # Login the new user after successful registration

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
                    'user_id': user.user_ID,
                    'first_name': user.first_name,
                    'last_name': user.last_name
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

# Get the current user's profile
@app.route('/api/v1/profile', methods=['GET'])
@login_required
def get_my_profile():
    # Query the profile table
    profile = Profile.query.filter_by(user_ID = current_user.user_ID).first()

    if profile: #If the profile exists, return all information
        return jsonify({
        'profile_ID':                    profile.profile_ID, #Change
        'user_ID':                       profile.user_ID,
        'date_of_birth':                 profile.date_of_birth.isoformat(),
        'gender':                        profile.gender,
        'bio':                           profile.bio,
        'location':                      profile.location,
        'visibility_status':             profile.visibility_status,
        'picture':                       profile.picture_filename,
        'gender_preference':             profile.gender_preference,
        'wants_children':                profile.wants_children,
        'relationship_type_preference':  profile.relationship_type_preference,
        'age':                           profile.age
    }), 200

    return jsonify({'error': 'Profile not found'}), 404





@app.route('/api/v1/profile', methods=['PUT'])
@login_required
def update_profile():
    form = ProfileForm()

    if form.validate_on_submit():
        # Get current profile
        profile = Profile.query.filter_by(user_ID = current_user.user_ID).first()

        if profile:
            # Update profile info
            profile.bio = form.bio.data
            profile.location = form.location.data
            profile.gender = form.gender.data
            profile.gender_preference = form.gender_preference.data
            profile.wants_children = form.wants_children.data
            profile.visibility_status = form.visibility_status.data
            profile.relationship_type_preference = form.relationship_type_preference.data
            
            # Profile picture
            picture = form.picture.data

            if picture: # If a file has been added
                filename = secure_filename(picture.filename)
                upload_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                picture.save(upload_path)
                profile.picture_filename = filename
            
            db.session.commit()
            return jsonify({
                'message': 'Profile Update Sucessful'
            }), 200
        
        else:
            return jsonify({'error': 'Profile not found'}), 404

    return jsonify({'errors': form_errors(form)}), 400




@app.route('/api/v1/profile/<int:profile_id>', methods=['GET'])
@login_required
def get_profile(profile_id):

    # Query the profile
    profile = Profile.query.filter_by(profile_ID = profile_id).first()

    if profile:
        return jsonify({
        'profile_ID':                    profile.profile_ID, #fix
        'user_ID':                       profile.user_ID,
        'date_of_birth':                 profile.date_of_birth.isoformat(),
        'gender':                        profile.gender,
        'bio':                           profile.bio,
        'location':                      profile.location,
        'visibility_status':             profile.visibility_status,
        'picture':                       profile.picture_filename,
        'gender_preference':             profile.gender_preference,
        'wants_children':                profile.wants_children,
        'relationship_type_preference':  profile.relationship_type_preference,
        'age':                           profile.age
    }), 200

    return jsonify({'error': 'Profile not found'}), 404

@app.route('/api/v1/user/search', methods=['GET'])
@login_required
def searchUsers():
    searchTerm = request.args.get('searchTerm','').strip()
    filt1 = request.args.get('filter1')
    filt2 = request.args.get('filter2')
    filt3 = request.args.get('filter3')
    filt4 = request.args.get('filter4')
    sort = request.args.get('sort')
    
    options = {"ASC": User.first_name, "DSC": User.first_name.desc(), "Age": Profile.age, "date_created": User.created_at}
    
    current = db.session.query(User, Profile).join(Profile, User.user_ID == Profile.user_ID).filter(Profile.visibility_status == "Public").order_by(options.get(sort, User.first_name))
    
    if searchTerm:
        current = current.filter(User.user_name.ilike(f"%{searchTerm}%"))
        
    if filt1 and filt1 != "none":
        today = date.today()
        if filt1 == ">41":
            max_dob = today - timedelta(days=42 * 365.25)
            current = current.filter(Profile.date_of_birth <= max_dob)
        else:
            start, end = map(int, filt1.split("-"))
            latest_dob = today - timedelta(days=start * 365.25)
            earliest_dob = today - timedelta(days=(end + 1) * 365.25)
        
            current = current.filter(Profile.date_of_birth.between(earliest_dob, latest_dob))
            
    if filt2 and filt2 != "none":
        current = current.filter(Profile.gender == filt2)
        
    if filt3 and filt3 != "none":
        current = current.filter(Profile.location == filt3)
        
    if filt4 and filt4 != "none":
        current = current.join(UserInterest, UserInterest.user_ID == Profile.user_ID).join(Interest, UserInterest.interest_ID == Interest.interest_ID).filter(Interest.name == filt4)
        
    res = current.all()
    
    return jsonify([{
        "username": use.user_name,
        "f_name": use.first_name,
        "l_name": use.last_name,
        "gender": prof.gender,
        "age": prof.age,
        "location": prof.location,
        "photo": f"/api/v1/images/{prof.picture_filename}"
        } for (use, prof) in res]), 200




@app.route('/api/v1/user/bookmarks', methods=['GET'])
@login_required
def getBookmarkedUsers():

    bookmarks = db.session.execute(db.select(Profile, User).join(Bookmarks, Bookmarks.Profile_ID == Profile.profile_ID).join(User, User.user_ID == Bookmarks.user_ID).where(current_user.user_ID == Bookmarks.user_ID, Profile.visibility_status == "Public")).all()

    return jsonify([{
        "username": u.user_name,
        "f_name": u.first_name,
        "l_name": u.last_name,
        "gender": p.gender,
        "age": p.age,
        "location": p.location,
        "photo": f"/api/v1/images/{p.picture_filename}"} for (p,u) in bookmarks]), 200

@app.route('/api/v1/user/bookmarks/<int:profile_ID>', methods=['DELETE'])
@login_required
def deleteBookmarkedUser(profile_ID):
    delete_Bookmark = True
    res = db.session.execute(db.select(Bookmark).where(Bookmarks.user_ID == current_user.user_ID, Bookmarks.Profile_ID == profile_ID))
    
    if not res:
        delete_Bookmark = False
    
    db.session.delete()
    db.session.commit()

    return jsonify({"message": "Bookmark deleted successfully."}), 200

@app.route('/api/v1/user/bookmarks/<int:profile_ID>', methods=['POST'])
@login_required
def addBookmarkedUser(profile_ID):
    make_Bookmark = True
    res = db.session.execute(db.select(Bookmark).where(Bookmarks.user_ID == current_user.user_ID, Bookmarks.Profile_ID == profile_ID))
    
    if res:
        make_Bookmark = False
    
    bookmark = Bookmarks(user_ID = current_user.user_ID, Profile_ID =profile_ID)
    
    db.session.add(bookmark)
    db.session.commit()

    return jsonify({"message": "Bookmark added successfully.",
                    "makeBookmark": make_Bookmark}), 201





@app.route('/api/v1/matches', methods=['GET'])
@login_required
def matching_algorithm():
    # Retrieve the current user's profile and interests
    current_profile = db.session.execute(db.select(Profile).where(Profile.user_ID == current_user.user_ID)).scalar_one()
    current_interests = db.session.execute(db.select(UserInterest.interest_ID).where(UserInterest.user_ID == current_user.user_ID)).scalars().all()

    # Remove profiles already liked/disliked
    removed_IDs = db.session.execute(db.select(Likes.liked_user_ID).where (Likes.user_ID == current_user.user_ID)).scalars().all()

    # Get all other users
    potential_matches = db.session.execute(
    db.select(User, Profile)
    .join(Profile, Profile.user_ID == User.user_ID) 
    .where(User.user_ID != current_user.user_ID)
    .where(Profile.visibility_status == "Public")
    .where(User.user_ID.notin_(removed_IDs))
    ).all()

    # Call matching algorithm
    matches = []

    for other, profile in potential_matches:
        # Get user intesest
        interests = db.session.execute(db.select(UserInterest.interest_ID). where(UserInterest.user_ID == other.user_ID))

        score = calc_score(current_profile, current_interests, profile, interests)

        matches.append({

                "user_ID": other.user_ID,
                "f_name": other.first_name,
                "l_name": other.last_name,
                "username": other.user_name,
                "age": profile.age,
                "bio": profile.bio,
                "gender": profile.gender,
                "location": profile.location,
                "photo": f"/api/v1/images/{profile.picture_filename}",
                "score": score,
                "percentage": round(((score/11.5) * 100), 2) # FIX THIS
            })

    matches.sort(key=lambda m: m["score"], reverse=True)
    
    return jsonify(matches),200 

    


@app.route('/api/v1/<int:user_ID>/bookmarks', methods=['GET'])
@login_required
def get_bookmarked_users(user_ID):
    bookmarks = db.session.execute(db.select(Bookmarks)).where(Bookmarks.user_ID == user_ID).scalars().all()

    return jsonify(bookmarks = bookmarks), 200




@app.route('/api/v1/<int:user_ID>/bookmarks', methods=['GET'])
@login_required
def get_bookmarks(user_ID):
    bookmarks = db.session.execute(
        db.select(Profile)).join(Bookmarks, Bookmarks.profile_ID == Profile.profile_ID).where(Bookmarks.user_ID == user_ID).scalars().all()

    return jsonify(bookmarks = bookmarks), 200




# Used when the User sets their interests right after registering
@app.route('/api/v1/profile/interest', methods = ['POST'])
@login_required
def interest():
    pass




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# CSRF
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})



@app.route('/api/v1/images/<filename>')
def uploads(filename):
    #upload_folder = os.path.join(os.getcwd(), 'uploads')
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)



@login_manager.unauthorized_handler
def unauthorized():
    return jsonify({'errors': [{'message': 'Unauthorized'}]}), 401

###
# The functions below should be applicable to all Flask apps.
###


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


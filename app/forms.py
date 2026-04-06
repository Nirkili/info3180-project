from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Email, Length, EqualTo, ValidationError
from flask_wtf.file import FileField, FileRequired, FileAllowed
from datetime import date



# Custom Functions

def validate_age(form, field):
  if field.data:
    today = date.today()
    dob = field.data
    age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
    if age < 18:
      raise ValidationError('You must be at least 18 years old to register')



class RegisterForm(FlaskForm):
  first_name = StringField('First Name', validators=[InputRequired()])
  last_name = StringField('Last Name', validators=[InputRequired()]) 

  username = StringField('Username', validators=[InputRequired()])
  email = StringField('Email', validators=[InputRequired(), Email()])

  date_of_birth = DateField('Date of Birth', validators=[InputRequired(), validate_age])

  password = PasswordField('Password', validators=[InputRequired(), Length(min=8, message='Password must be at least 8 characters long')])
  confirmation = PasswordField('Confirm Password', validators=[InputRequired(), EqualTo('password', message='Passwords must match')])

  gender = SelectField('Gender', choices=[
    ('', 'Select gender'),
    ('Female',     'Female'),
    ('Male',       'Male'),
    ('Non-binary', 'Non-binary')
  ], validators=[InputRequired()])

  gender_preference = SelectField('Interested In', choices=[
      ('', 'Select preference'),
      ('Female',     'Female'),
      ('Male',       'Male'),
      ('Non-binary', 'Non-binary')
  ], validators=[InputRequired()])

  relationship_preference = SelectField('Looking For', choices=[
      ('', 'Select type'),
      ('Casual',  'Casual'),
      ('Serious', 'Serious')
  ], validators=[InputRequired()])

  wants_children = SelectField('Do You Want Children?', choices=[
      ('', 'Select an option'),
      ('Wants Children', 'Wants Children'),
      ('Does Not Want Children', 'Does Not Want Children')
  ], validators=[InputRequired()])
  
  

class LoginForm(FlaskForm):
  username = StringField('Username', validators=[InputRequired()])
  password = PasswordField('Password', validators=[InputRequired()])
  

class ProfileForm(FlaskForm): # Used when a user wants to edit their profile information
    bio      = TextAreaField('About Me')
    location = StringField('Location')

    gender = SelectField('Gender', choices=[
    ('', 'Select gender'),
    ('Female',     'Female'),
    ('Male',       'Male'),
    ('Non-binary', 'Non-binary')
  ], validators=[InputRequired()])

    gender_preference = SelectField('Interested In', choices=[
        ('', 'Select preference'),
        ('Female',     'Female'),
        ('Male',       'Male'),
        ('Non-binary', 'Non-binary')
    ], validators=[InputRequired()])

    wants_children = SelectField('Do You Want Children?', choices=[
        ('', 'Select an option'),
        ('Wants Children',          'Wants Children'),
        ('Does Not Want Children',  'Does Not Want Children')
    ])

    visibility_status = SelectField('Profile Visibility', choices=[
        ('Public',  'Public'),
        ('Private', 'Private')
    ])

    relationship_type_preference = SelectField('Looking For', choices=[
      ('', 'Select type'),
      ('Casual',  'Casual'),
      ('Serious', 'Serious')
    ], validators=[InputRequired()])

    picture = FileField('Profile Picture', validators=[ FileAllowed(['jpg', 'jpeg', 'png'], 'Images only')])

    interests = StringField('Interests')



from . import db
import enum
from sqlalchemy.dialects import postgresql
from datetime import datetime

# ENUM CLASSES
class Gender(str, enum.Enum):
  FEM = "Female"
  MALE = "Male"
  NB = "Non-binary"
  
class VisibilityStatus(str, enum.Enum):
  PRIVATE = "Private"
  PUBLIC = "Public"

class RelationshipPreference(str, enum.Enum):
  CASUAL = "Casual"
  SERIOUS = "Serious"
  
class ChildrenPreference(str, enum.Enum):
  DOES_WANT = "Wants Children"
  DOES_NOT = "Does Not Want Children"

class LikeType(str, enum.Enum):
  LIKE = "Like"
  DISLIKE = "Dislike"
  PASS = "Pass"



# BASE CLASSES
class User(db.Model): # Base User Class

  __tablename__ = 'User'
  
  user_ID = db.Column(db.Integer, primary_key=True)

  # Basic Personal Information
  first_name = db.Column(db.String(100), nullable=False)
  last_name = db.Column(db.String(100), nullable=False)

  # User Credentials
  user_name = db.Column(db.String(100), unique=True, nullable=False)
  email = db.Column(db.String(100), unique=True, nullable=False)
  password = db.Column(db.String(255), nullable=False)
  created_at = db.Column(db.DateTime, default=datetime.now)


  profile = db.relationship('Profile', backref='user', uselist=False)



# PROFILE CLASS
class Profile(db.Model):

  __tablename__ = 'Profile'

  # Used to identify User
  profile_ID = db.Column(db.Integer, primary_key=True)
  user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False)
  
  # Other User Details
  age = db.Column(db.Integer, nullable=False)
  gender = db.Column(postgresql.ENUM(Gender, name="gender"), nullable=False)
  bio = db.Column(db.Text)
  
  location = db.Column(db.String(100), nullable=False, index=True)
  visibility_status = db.Column(postgresql.ENUM(VisibilityStatus, name = "account_status"), nullable = False)
  
  picture_filename = db.Column(db.String(100), nullable=False)
  
  # Preferences 
  gender_preference = db.Column(postgresql.ENUM(Gender, name = "gender_preference"), nullable = False)
  wants_children = db.Column(postgresql.ENUM(ChildrenPreference, name = "children_preference"), nullable = False)
  relationship_type_preference = db.Column(postgresql.ENUM(RelationshipPreference, name = "relationship_preference"), nullable = False)
  
  
  
# INTEREST CLASS
class Interest(db.Model):

  __tablename__ = 'Interest'
  
  interest_ID = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)

# USER INTEREST CLASS
class UserInterest(db.Model):
  
  __tablename__ = 'UserInterest'
  
  user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False, primary_key=True)
  interest_ID = db.Column(db.Integer, db.ForeignKey('Interest.interest_ID'), nullable=False, primary_key=True)
  


# LIKES CLASS
class Likes(db.Model):

  __tablename__ = 'Likes'
  
  like_ID = db.Column(db.Integer, primary_key=True)
  user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False, index=True)
  liked_user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False, index=True)

  type = db.Column(postgresql.ENUM(LikeType, name="like_type"), nullable=False)

  created_at = db.Column(db.DateTime, default=datetime.now)



# MATCH CLASS
class Match(db.Model):

  __tablename__ = 'Match'
  
  user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False, primary_key=True)
  match_user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False, primary_key = True)



# BOOKMARKS CLASS
class Bookmarks(db.Model):

  __tablename__ = "Bookmarks"
  
  user_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), primary_key=True)
  Profile_ID = db.Column(db.Integer, db.ForeignKey('Profile.profile_ID'), primary_key=True)
  date_created = db.Column(db.DateTime, default=datetime.now, nullable = False)



# CHAT CLASS
class Chat(db.Model):

  __tablename__ = "Chat"
  chat_ID = db.Column(db.Integer, primary_key = True)
  user1_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False)
  user2_ID = db.Column(db.Integer, db.ForeignKey('User.user_ID'), nullable=False)

  date_created = db.Column(db.DateTime, default=datetime.now)

  messages = db.relationship('Message', backref='chat', lazy=True)



# MESSAGE CLASS
class Message (db.Model):

  __tablename__ = "Message"

  message_ID = db.Column(db.Integer, primary_key=True)

  chat_ID = db.Column(db.Integer, db.ForeignKey("Chat.chat_ID"), nullable = False)
  sender_ID = db.Column(db.Integer, db.ForeignKey("User.user_ID"), nullable = False)

  content = db.Column(db.Text, nullable = True)
  timestamp = db.Column(db.DateTime, default=datetime.now)


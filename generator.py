from faker import Faker
import random
from app import db, app
from app.models import User, Profile, Interest, UserInterest

fake = Faker()
def genData():
        with app.app_context():
            try:
                gender_options = ["Male", "Female", "Non-binary"]
                parishes = ["Kingston", "St. Andrew", "St. Thomas", "Portland", "St. Mary", "St. Ann", "Trelawny", "St. James", "Hanover", "Westmoreland", "St. Elizabeth", "Manchester", "Clarendon", "St. Catherine"]
                
                all_interests = Interest.query.all()

                for i in range(100):
                    fname = fake.first_name()
                    lname = fake.last_name()
                    
                    new_user = User(
                        first_name=fname,
                        last_name=lname,
                        user_name=f"{fname.lower()}{lname.lower()}{i}",
                        email=fake.unique.email(),
                        password=f"pass123{i}"
                    )
                    
                    db.session.add(new_user)
                    db.session.flush() 

                    new_profile = Profile(
                        user_ID=new_user.user_ID,
                        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                        gender=random.choice(gender_options),
                        bio=fake.sentence(nb_words=12),
                        location=random.choice(parishes),
                        visibility_status=random.choice(["Public", "Private"]),
                        picture_filename="default.jpg",
                        gender_preference=random.choice(gender_options),
                        wants_children=random.choice(["Wants Children", "Does Not Want Children"]),
                        relationship_type_preference=random.choice(["Casual","Serious"])
                    )
                    db.session.add(new_profile)

                    user_interests = random.sample(all_interests, random.randint(1, 5))
                    for interest in user_interests:
                        ui = UserInterest(user_ID=new_user.user_ID, interest_ID=interest.interest_ID)
                        db.session.add(ui)

                db.session.commit()
                print("Successfully added 100 users!")

            except Exception as e:

                db.session.rollback()
                print(f"Transaction failed. Error: {e}")
            
def genInterests():
    interests_list = [
    "Yoga", "Meditation", "Hiking", "Swimming", "Gardening",
    "Cooking", "Baking", "Pets", "Fashion", "Fitness",
    "Writing", "Blogging", "Entrepreneurship", "Investing", "Photography",
    "Art", "Reading", "Learning", "Travel", "Volunteering",
    "Gaming", "Movies", "Anime", "Music", "Social Media",
    "Cars", "Tech", "Science", "Coding", "Knitting"
    ]
    
    with app.app_context():
        try:
            for interest in interests_list:
                db.session.add(Interest(name = interest))
            
            db.session.commit()
            
        except Exception as e:
                db.session.rollback()
                print(f"Transaction failed. Error: {e}")
    

if __name__ == "__main__":
    with app.app_context():
        db.session.execute(db.text('TRUNCATE TABLE "User", "Profile", "UserInterest", "Interest" RESTART IDENTITY CASCADE;'))
        db.session.commit()
    genInterests()
    genData()
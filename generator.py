from faker import Faker
import random
from app import db, app, bcrypt
from app.models import *
 

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
                    username = f"{fname.lower()}{lname.lower()}{i}"
                    email = f"{fname.lower()}.{lname.lower()}{random.randint(1, 999)}@gmail.com"
                    plain_password = f"pass123"

                    new_user = User(
                        first_name=fname,
                        last_name=lname,
                        user_name= username,
                        email=email,
                        password = bcrypt.generate_password_hash(plain_password).decode('utf-8')
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

                    current_interests = db.session.execute(db.select(Interest.name).join(UserInterest, UserInterest.interest_ID == Interest.interest_ID).where(UserInterest.user_ID == new_user.user_ID)).scalars().all()
                    
                    line = f"{fname}, {lname}, {email}, {plain_password}\n Interests: "
                    
                    for i in current_interests:
                        line += f"{i},"
                    
                db.session.commit()
                
                all_users = User.query.all()
                all_profiles = Profile.query.all()
                
                credentials = []
                for user in all_users:
                    # Find this user's specific profile_ID
                    user_profile = next(p for p in all_profiles if p.user_ID == user.user_ID)
                    line = f"{user.first_name}, {user.last_name}, {user.email}\n"
                    
                    # Now this will actually find the other 99 users
                    lineAdd = genBookmarks(user.user_ID, user_profile.profile_ID)
                    credentials.append(line + lineAdd)
                    
                print("Successfully added 100 users!")
                return credentials

                

            except Exception as e:

                db.session.rollback()
                print(f"Transaction failed. Error: {e}")
            
def genInterests():
    interests_list = ["Coding", "Investing","Entrepreneurship","Fitness","Meditation","Reading","Learning","Writing","Photography","Tech","Science","Travel","Cooking","Music","Social Media"]
    
    with app.app_context():
        try:
            for interest in interests_list:
                db.session.add(Interest(name = interest))
            
            db.session.commit()
        
        except Exception as e:
                db.session.rollback()
                print(f"Transaction failed. Error: {e}")
                
def genBookmarks(user_ID, profile_ID):
    profiles = db.session.execute(db.select(Profile).where(Profile.profile_ID != profile_ID, Profile.user_ID != user_ID)).scalars().all()

    user_bookmarks = random.sample(profiles, random.randint(1, 20))

    lineAdd = "Bookmarked: "

    for i in user_bookmarks:
        b = Bookmarks(user_ID=user_ID, Profile_ID= i.profile_ID)
        db.session.add(b)

    # Get names of bookmarked users
    booked = db.session.execute(
        db.select(User.first_name, User.last_name)
        .join(Profile, Profile.user_ID == User.user_ID)
        .join(Bookmarks, Bookmarks.Profile_ID == Profile.profile_ID)
        .where(Bookmarks.user_ID == user_ID)
    ).all()

    for first, last in booked:
        lineAdd += f"{first} {last}, "

    lineAdd += "\n"
    return lineAdd
        

if __name__ == "__main__":
    with app.app_context():
        db.session.execute(db.text('TRUNCATE TABLE "User", "Profile", "UserInterest", "Interest", "Bookmarks" RESTART IDENTITY CASCADE;'))
        db.session.commit()
    genInterests()
    users = genData()

    # Write to file

    with open('credentials.txt', "w", encoding="utf-8") as f:
        for i in users:
            f.write(i)
            
        
    print("created file")


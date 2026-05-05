from faker import Faker
import random
from app import db, app, bcrypt
from app.models import *
 

fake = Faker()
def gen_users_profiles():
        with app.app_context():
            try:
                gender_options = ["Male", "Female", "Non-binary"]
                parishes = ["Kingston", "St. Andrew", "St. Thomas", "Portland", "St. Mary", "St. Ann", "Trelawny", "St. James", "Hanover", "Westmoreland", "St. Elizabeth", "Manchester", "Clarendon", "St. Catherine"]

                credentials = []

                for i in range(100):
                    gender = random.choice(gender_options)

                    if gender == "Female":fname = fake.first_name_female()
                    elif gender == 'Male': fname = fake.first_name_male()
                    else:fname = fake.first_name()

                    lname = fake.last_name()
                    username = f"{fname.lower()}{lname.lower()}{i}"
                    email = f"{fname.lower()}.{lname.lower()}{random.randint(1, 999)}@gmail.com"
                    plain_password = f"pass123{i}"
                    created_on = fake.date_time_this_year()
                    visibility = random.choices(["Public", "Private"], weights=[80, 20], k=1)[0]

                    credentials.append(f"User: {fname} {lname}, {email}, {plain_password}, {created_on}\n")

                    new_user = User(
                        first_name=fname,
                        last_name=lname,
                        user_name= username,
                        email=email,
                        password = bcrypt.generate_password_hash(plain_password).decode('utf-8'),
                        created_at=created_on
                    )
                    
                    db.session.add(new_user)
                    db.session.flush() 

                    new_profile = Profile(
                        user_ID=new_user.user_ID,
                        date_of_birth=fake.date_of_birth(minimum_age=18, maximum_age=60),
                        gender=gender,
                        bio=fake.sentence(nb_words=12),
                        location=random.choice(parishes),
                        visibility_status= visibility,
                        picture_filename="default.jpg",
                        gender_preference= random.choice(gender_options),
                        wants_children=random.choice(["Wants Children", "Does Not Want Children"]),
                        age_preference=random.choice(['18-24', '25-29', '30-40', '>40']),                        
                        relationship_type_preference=random.choice(["Casual","Serious"]),
                        radius_preference=random.choice(['25', '50', '100', '250'])
                    )
                    db.session.add(new_profile)

                db.session.commit()
                print("Successfully added 100 users!")
                return credentials

            except Exception as e:

                db.session.rollback()
                print(f"1Transaction failed. Error: {e}")
            
def genInterests():
    interests_list = ["Coding", "Investing","Entrepreneurship","Fitness","Meditation","Reading","Learning","Writing","Photography","Tech","Science","Travel","Cooking","Music","Social Media"]
    
    with app.app_context():
        try:
            for interest in interests_list:
                db.session.add(Interest(interest_name = interest))
            
            db.session.commit()
            
        except Exception as e:
                db.session.rollback()
                print(f"2Transaction failed. Error: {e}")
                
def gen_user_interests(user_ID1):
    all_interests = Interest.query.all()
    
    user_interests = random.sample(all_interests, random.randint(1, 5))
    for interest in user_interests:
        ui = UserInterest(user_ID=user_ID1, interest_ID=interest.interest_ID)
        db.session.add(ui)
        
    db.session.commit()

def gen_Likes(user_ID):
    match = False

    users = db.session.execute(db.select(User).where(User.user_ID != user_ID)).scalars().all()
    
    user_likes = random.sample(users, random.randint(1, 10))
    
    for i in user_likes:
        l = Interaction(user_ID=user_ID, other_user_ID=i.user_ID, type=random.choice(["Like", "Pass"]))
        db.session.add(l) 

        #Check to see if there is a match
        mutual_like = db.session.execute(db.select(Interaction).where(Interaction.user_ID == user_ID, Interaction.other_user_ID == user_ID, Interaction.type == "Like")).scalar_one_or_none()

        if(mutual_like):
            existing_match = db.session.execute(db.select(Match).where(
                db.or_(
                    db.and_(Match.user_ID == user_ID, Match.match_user_ID == user_ID),
                    db.and_(Match.user_ID == user_ID, Match.match_user_ID == user_ID))
            )).scalar_one_or_none()

            # Else make a new entry in the Match table
            if not existing_match:
                match = True
                new_match = Match(
                    user_ID = user_ID,
                    match_user_ID = user_ID
                )

                new_chat = Chat(
                    user1_ID=user_ID,
                    user2_ID=user_ID)
                
                db.session.add(new_match)
                db.session.add(new_chat)

         
    db.session.commit()

    return match
    
def genBookmarks(user_ID, profile):
    print(f"Generating bookmarks for user_ID: {user_ID}")
    profiles = db.session.execute(db.select(Profile).where(Profile.profile_ID != profile.profile_ID, Profile.user_ID != user_ID)).scalars().all()

    user_bookmarks = random.sample(profiles, random.randint(1, 10))
    print(f"User {user_ID} will bookmark profile IDs: {[p.profile_ID for p in user_bookmarks]}")
    for i in user_bookmarks:
        b = Bookmarks(user_ID=user_ID, Profile_ID= i.profile_ID)
        db.session.add(b)
    db.session.commit()
    
def write_to_file(credentials, filename):
    with open(filename, 'w') as f:
        with app.app_context():
            f.write("Generated User Credentials:\n")
            for i in credentials:
                f.write(i)
                

if __name__ == "__main__":
    with app.app_context():
        db.session.execute(db.text('TRUNCATE TABLE "User", "Profile", "UserInterest", "Interest", "Bookmarks" RESTART IDENTITY CASCADE;'))
        db.session.commit()
    genInterests()
    print("Interests generated successfully.")
    credentials = gen_users_profiles()
    matches = []
    print("Users and profiles generated successfully.")
    
    with app.app_context():
        users1 = db.session.execute(db.select(User)).scalars().all()
        
        for user in users1:   
            gen_user_interests(user.user_ID)
            genBookmarks(user.user_ID, user.profile)
            has_match = gen_Likes(user.user_ID)


            matches.append((f"{user.first_name} {user.last_name}, has Match = {has_match}\n"))
    
    write_to_file(credentials, "credentials.txt")
    write_to_file(matches, 'has_match.txt')
    print(f"Generated interests, likes, and bookmarks for users")



from faker import Faker
import random
from app import db, app, bcrypt
from app.models import User, Profile, Interest, UserInterest
 

fake = Faker()
def genData():
        with app.app_context():
            try:
                gender_options = ["Male", "Female", "Non-binary"]
                parishes = ["Kingston", "St. Andrew", "St. Thomas", "Portland", "St. Mary", "St. Ann", "Trelawny", "St. James", "Hanover", "Westmoreland", "St. Elizabeth", "Manchester", "Clarendon", "St. Catherine"]
                
                all_interests = Interest.query.all()

                credentials = []

                for i in range(100):
                    gender = random.choice(gender_options)

                    if gender == "Female":fname = fake.first_name_female()
                    elif gender == 'Male': fname = fake.first_name_male()
                    else:fname = fake.first_name()

                    print(fname)


                    lname = fake.last_name()
                    username = f"{fname.lower()}{lname.lower()}{i}"
                    email = f"{fname.lower()}.{lname.lower()}{random.randint(1, 999)}@gmail.com"
                    plain_password = f"pass123{i}"
                    visibility = random.choices(["Public", "Private"], weights=[80, 20], k=1)[0]
                    print(f"{fname}, {visibility}")
                    
                    credentials.append(f"{email}, {plain_password}\n")

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
                        gender=gender,
                        bio=fake.sentence(nb_words=12),
                        location=random.choice(parishes),
                        visibility_status= visibility,
                        picture_filename="default.jpg",
                        gender_preference=random.choice(gender_options),
                        wants_children=random.choice(["Wants Children", "Does Not Want Children"]),
                        age_preference=random.choice(['Young_Adult', 'Adult', 'MiddleAged', 'Old']),                        relationship_type_preference=random.choice(["Casual","Serious"]),
                        radius_preference=random.choice(['25', '50', '100', '300'])
                    )
                    db.session.add(new_profile)

                    user_interests = random.sample(all_interests, random.randint(1, 5))
                    for interest in user_interests:
                        ui = UserInterest(user_ID=new_user.user_ID, interest_ID=interest.interest_ID)
                        db.session.add(ui)

                db.session.commit()
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
    

if __name__ == "__main__":
    with app.app_context():
        db.session.execute(db.text('TRUNCATE TABLE "User", "Profile", "UserInterest", "Interest" RESTART IDENTITY CASCADE;'))
        db.session.commit()
    genInterests()
    users = genData()

    # Write to file

    with open('credentials.txt', "w", encoding="utf-8") as f:
         for i in users:
              f.write(i)
    print("created file")


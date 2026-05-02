    users = db.session.execute(db.select(User)).scalars().all()
        for user in users:   
            gen_user_interests(user.user_ID)
            genBookmarks(user.user_ID, user.profile_ID)
            gen_Likes(user.user_ID, user.profile_ID)
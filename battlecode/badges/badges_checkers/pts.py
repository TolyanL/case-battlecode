def check_pts(user_profile: object) -> str:
    if user_profile.pts >= 100:
        return "rookie"
    elif user_profile.pts >= 500:
        return "recruit"
    elif user_profile.pts >= 1500:
        return "apprentice"
    elif user_profile.pts >= 2000:
        return "journeyman"
    elif user_profile.pts >= 2500:
        return "adept"
    elif user_profile.pts >= 3000:
        return "specialist"
    elif user_profile.pts >= 3500:
        return "expert"
    elif user_profile.pts >= 4000:
        return "champion"
    elif user_profile.pts >= 4500:
        return "master"
    elif user_profile.pts >= 5000:
        return "grandmaster"

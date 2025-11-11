from UserProfile import UserProfile

class CreateUserProfile:
    def __init__(self):
        self.user_profile = UserProfile()

    def createUserProfile(self, profile, description, profileState):
        response = self.user_profile.createUserProfile(profile, description, profileState)
        return response
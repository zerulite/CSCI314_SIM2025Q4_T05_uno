from UserProfile import UserProfile

class ViewUserProfile:
    def __init__(self):
        self.user_entity = UserProfile()
    
    def viewUserProfile(self, profile):
        return self.user_entity.viewUserProfile(profile)
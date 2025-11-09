from UserProfile import UserProfile

class ViewUserProfile:
    def __init__(self):
        self.user_entity = UserProfile()
    
    def view_user_profile(self, profile):
        return self.user_entity.view_profile(profile)
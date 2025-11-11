from UserProfile import UserProfile

class UpdateUserProfile:
    def __init__(self):
        self.user_profile = UserProfile()
        
    def getProfile(self, profile):
        profile_data = self.user_profile.view_profile(profile)
        return profile_data
    
    def updateUserProfile(self, profile, description, profileState):
        response = self.user_profile.updateUserProfile(profile, description, profileState)
        return response
    

from UserProfile import UserProfile

class SuspendUserProfile:
    def __init__(self):
        self.user_account = UserProfile()
        
    def getProfile(self, profile):
        user_data = self.user_account.viewUserProfile(profile)
        return user_data
    
    def suspendUserProfile(self, profile, profileState):
        response = self.user_account.suspendUserProfile(profile, profileState)
        return response
    

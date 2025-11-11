from UserAccount import UserAccount

class UpdateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()
    
    def checkProfile(self, profile):
        response = self.user_account.check_profile(profile)
        return response
        
    def getUserByID(self, userID):
        user_data = self.user_account.viewUserAccount(userID)
        return user_data
    
    def updateUserAccount(self, userID, password, name, email, profile, userState):
        profile_check = self.checkProfile(profile)
        if not profile_check["success"]:
            return {"message": profile_check["message"]}

        response = self.user_account.updateUserAccount(userID, password, name, email, profile, userState)
        return response
    

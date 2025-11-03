from UserAccount import UserAccount

class UpdateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()
        
    def getUserByID(self, userID):
        user_data = self.user_account.view_acct(userID)
        return user_data
    
    def updateUserAccount(self, userID, password, name, email, profile, userState):
        response = self.user_account.update_acct(userID, password, name, email, profile, userState)
        return response
    

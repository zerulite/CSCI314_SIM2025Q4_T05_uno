from UserAccount import UserAccount

class SuspendUserAccount:
    def __init__(self):
        self.user_account = UserAccount()
        
    def getUserByID(self, userID):
        user_data = self.user_account.viewUserAccount(userID)
        return user_data
    
    def suspendUserAccount(self, userID, userState):
        response = self.user_account.suspendUserAccount(userID, userState)
        return response
    

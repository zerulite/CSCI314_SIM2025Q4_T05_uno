from UserAccount import UserAccount

class SuspendUserAccount:
    def __init__(self):
        self.user_account = UserAccount()
        
    def getUserByID(self, userID):
        user_data = self.user_account.view_acct(userID)
        return user_data
    
    def suspendUserAccount(self, userID, userState):
        response = self.user_account.suspend_acct(userID, userState)
        return response
    

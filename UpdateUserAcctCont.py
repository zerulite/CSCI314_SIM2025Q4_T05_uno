from UserAccount import UserAccount

class UpdateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()
        
    def updateUserAccount(userID, password, name, email, profile, userState):
        uua = UserAccount()
        response = uua.update_acct(userID, password, name, email, profile, userState)
        return response

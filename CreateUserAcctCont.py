from UserAccount import UserAccount

class CreateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()

    def createUserAccount(self, userID, password, name, email, profile, userState):
        response = self.user_account.create_acct(userID, password, name, email, profile, userState)
        return response
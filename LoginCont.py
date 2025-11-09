from UserAccount import UserAccount

class Login:
    def __init__(self):
        self.user_account = UserAccount()

    def loginUser(self, userID, password):
        return self.user_account.login(userID, password)

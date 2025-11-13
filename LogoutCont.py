from UserAccount import UserAccount

class Logout:
    def __init__(self):
        self.user_account = UserAccount()

    def logoutUser(self):
        return self.user_account.logoutUser()
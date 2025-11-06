from UserAccount import UserAccount

class CreateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()

    def check_profile(self, profile):
        response = self.user_account.check_profile(profile)
        return response

    def createUserAccount(self, userID, password, name, email, profile, userState):
        profile_check = self.check_profile(profile)
        if not profile_check["success"]:
            return {"message": profile_check["message"]}

        # Create the account if profile is active
        response = self.user_account.create_acct(userID, password, name, email, profile, userState)
        return response
from UserAccount import UserAccount

class CreateUserAccount:
    def __init__(self):
        self.user_account = UserAccount()

    def checkProfile(self, profile):
        response = self.user_account.check_profile(profile)
        return response

    def createUserAccount(self, userID, password, name, email, profile, userState):
        profile_check = self.checkProfile(profile)
        if not profile_check["success"]:
            return {"message": profile_check["message"]}

        # Create the account if profile is active
        response = self.user_account.createUserAccount(userID, password, name, email, profile, userState)
        return response
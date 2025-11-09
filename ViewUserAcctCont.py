from UserAccount import UserAccount

class ViewUserAccount:
    def __init__(self):
        self.user_entity = UserAccount()
    
    def viewUserAccount(self, user_id):
        return self.user_entity.view_acct(user_id)
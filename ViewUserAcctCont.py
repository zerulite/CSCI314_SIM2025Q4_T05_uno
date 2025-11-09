from UserAccount import UserAccount

class ViewUserAccount:
    def __init__(self):
        self.user_entity = UserAccount()
    
    def view_user_account(self, user_id):
        return self.user_entity.view_acct(user_id)
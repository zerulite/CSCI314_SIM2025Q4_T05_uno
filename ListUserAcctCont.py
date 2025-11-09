from UserAccount import *

class ListUserAccount:
    def __init__(self):
        self.user_entity = UserAccount()
    
    def list_acct(self):
        return self.user_entity.list_acct()

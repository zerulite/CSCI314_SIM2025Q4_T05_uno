from UserAccount import *

class ListUserAccount:
    def __init__(self):
        self.user_entity = UserAccount()
    
    def listAcct(self):
        return self.user_entity.listUserAccount()

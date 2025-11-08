from UserProfile import *

class ListUserProfile:
    def __init__(self):
        self.user_entity = UserProfile()
    
    def list_profile(self):
        return self.user_entity.list_profile()

from UserProfile import *

class SearchUserProfile:
    def __init__(self):
        self.user_entity = UserProfile()


    def search_profiles(self, search_fields: dict):
        #remove empty values
        search_fields = {k: v for k, v in search_fields.items() if v}
        # Call the entity method
        return self.user_entity.search_profiles(**search_fields)

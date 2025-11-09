from UserAccount import *

class SearchUserAccount:
    def __init__(self):
        self.user_entity = UserAccount()


    def search_users(self, search_fields: dict):
        #remove empty values
        search_fields = {k: v for k, v in search_fields.items() if v}
        # Call the entity method
        return self.user_entity.search_users(**search_fields)

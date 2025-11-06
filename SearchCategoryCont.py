from Category import Category

class SearchCategory:
    def __init__(self):
        self.category = Category()


    def search_category(self, search_fields: dict):
        #remove empty values
        search_fields = {k: v for k, v in search_fields.items() if v}
        # Call the entity method
        return self.category.search_category(**search_fields)

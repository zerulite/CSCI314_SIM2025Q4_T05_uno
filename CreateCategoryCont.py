from Category import Category

class CreateCategory:
    def __init__(self):
        self.category = Category()

    def create_category(self, category, description):
        response = self.category.create_category(category, description)
        return response
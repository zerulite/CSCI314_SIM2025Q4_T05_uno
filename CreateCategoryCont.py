from Category import Category

class CreateCategory:
    def __init__(self):
        self.category = Category()

    def createCategory(self, category, description):
        response = self.category.createCategory(category, description)
        return response
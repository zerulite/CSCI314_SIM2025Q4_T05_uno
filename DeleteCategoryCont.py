from Category import Category

class DeleteCategory:
    def __init__(self):
        self.category = Category()

    def deleteCategory(self, category):
        response = self.category.deleteCategory(category)
        return response
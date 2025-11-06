from Category import Category

class DeleteCategory:
    def __init__(self):
        self.category = Category()

    def delete_category(self, category):
        response = self.category.delete_category(category)
        return response
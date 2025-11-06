from Category import Category

class ViewCategory:
    def __init__(self):
        self.category = Category()
    
    def view_category(self, category):
        return self.category.view_category(category)
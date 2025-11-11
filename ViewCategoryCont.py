from Category import Category

class ViewCategory:
    def __init__(self):
        self.category = Category()
    
    def viewCategory(self, category):
        return self.category.viewCategory(category)
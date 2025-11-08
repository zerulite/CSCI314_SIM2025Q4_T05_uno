from Category import Category

class ListCategory:
    def __init__(self):
        self.category = Category()
    
    def listCategory(self):
        return self.category.list_category()

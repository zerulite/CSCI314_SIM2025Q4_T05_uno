from Category import Category

class UpdateCategory:
    def __init__(self):
        self.category = Category()
        
    def getCategory(self, category):
        category_data = self.category.view_category(category)
        return category_data
    
    def updateCategory(self, category, description):
        response = self.category.update_category(category, description)
        return response
    

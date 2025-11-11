from Category import Category

class UpdateCategory:
    def __init__(self):
        self.category = Category()
        
    def getCategory(self, category):
        category_data = self.category.viewCategory(category)
        return category_data
    
    def updateCategory(self, category, description):
        response = self.category.updateCategory(category, description)
        return response
    

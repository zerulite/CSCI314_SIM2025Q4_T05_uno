from Category import Category

class UpdateCategory:
    def __init__(self):
        self.category = Category()
        
    def get_category(self, category):
        category_data = self.category.view_category(category)
        return category_data
    
    def update_category(self, category, description):
        response = self.category.update_category(category, description)
        return response
    

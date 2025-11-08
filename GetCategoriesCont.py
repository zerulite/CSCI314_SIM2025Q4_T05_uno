from Request import Request

class GetCategoriesCont:
    def __init__(self):
        self.reqEntity = Request()
        
    def getCategoriesCont(self):
        # Return should always be list (empty or filled)
        result = self.reqEntity.getCategories()
        response = []

        for cat in result:
            response.append(cat[0])

        return response
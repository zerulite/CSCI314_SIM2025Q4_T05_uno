from Request import Request

class CSRSearchHistoryController:
    def __init__(self):
        self.request_entity = Request()

    def searchHistory(self, **filters):
        # Entity enforces completed='Yes'
        return self.request_entity.searchHistory(**filters)

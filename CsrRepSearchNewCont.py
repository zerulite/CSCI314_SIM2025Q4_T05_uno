from Request import Request

class CSRSearchNewController:
    def __init__(self):
        self.request_entity = Request()

    def searchNewRequests(self, **kwargs):
        return self.request_entity.search_new_request(**kwargs)
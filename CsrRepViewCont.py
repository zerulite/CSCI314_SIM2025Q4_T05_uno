from Request import Request

class CSRViewNewController:
    def __init__(self):
        self.request_entity = Request()

    def viewAllRequests(self, limit=100, offset=0):
        return self.request_entity.viewAllRequests(limit=limit, offset=offset)
from Request import Request

class CSRViewNewController:
    def __init__(self):
        self.request_entity = Request()

    def view_all_requests(self, limit=100, offset=0):
        return self.request_entity.view_all_requests(limit=limit, offset=offset)
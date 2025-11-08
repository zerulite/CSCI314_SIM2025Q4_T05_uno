from Request import Request

class CSRViewShortlistController:
    def __init__(self):
        self.request_entity = Request()

    def listShortlist(self, csr_user_id: str, limit=100, offset=0):
        return self.request_entity.view_shortlist(csr_user_id= csr_user_id, limit=limit, offset=offset)

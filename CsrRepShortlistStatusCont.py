from Request import Request

class CSRShortlistStatusController:
    def __init__(self):
        self.request_entity = Request()

    def addToShortlistStatus(self, request_id: str, csr_user_id: str) -> str:
        return self.request_entity.shortlist_status(request_id, csr_user_id)
from Request import Request

class CSRShortlistStatusController:
    def __init__(self):
        self.request_entity = Request()

    def shortlistStatus(self, request_id: str, csr_user_id: str) -> str:
        return self.request_entity.shortlistStatus(request_id, csr_user_id)
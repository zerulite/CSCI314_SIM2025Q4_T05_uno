from Request import Request

class CSRShortlistController:
    def __init__(self):
        self.request_entity = Request()

    def addToShortlist(self, request_id: str, csr_user_id: str) -> bool:
        # why: shortlist is per user, must pass csr's userID
        return self.request_entity.add_to_shortlist(request_id, csr_user_id)

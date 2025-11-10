from Request import Request

class CSRSearchShortlistController:
    def __init__(self):
        self.request_entity = Request()

    def searchShortlisted(self, csr_user_id: str, **filters):
        return self.request_entity.searchShortlisted(csr_user_id=csr_user_id, **filters)
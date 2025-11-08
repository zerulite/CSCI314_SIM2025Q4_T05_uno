from Request import Request

class CSRViewIndividualController:
    def __init__(self):
        self.request_entity = Request()

    def viewIndividualRequest(self, request_id: str):
        rows = self.request_entity.view_individual_request(request_id)
        return rows[0] if rows else None

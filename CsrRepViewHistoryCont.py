# CsrRepViewCompletedCont.py
from Request import Request

class CSRViewHistoryController:
    def __init__(self):
        self.request_entity = Request()

    def viewHistory(self, limit=100, offset=0):
        return self.request_entity.viewHistory(limit=limit, offset=offset)

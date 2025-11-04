from Request import Request

class CreateReqCont:
    def __init__(self):
        self.request = Request()

    def createReqCont(self, reqDescription: str, helpNeededDate: str, helpNeededTime: str, category: str, userID: str):
        response = self.request.createReq(reqDescription, helpNeededDate, helpNeededTime, category, userID)
        return response
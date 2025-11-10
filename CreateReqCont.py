from Request import Request

class CreateReqCont:
    def __init__(self):
        self.reqEntity = Request()

    def createReq(self, reqDescription: str, helpNeededDate: str, helpNeededTime: str, category: str, userID: str):
        result = self.reqEntity.createReq(reqDescription, helpNeededDate, helpNeededTime, category, userID)
        
        if isinstance(result, dict):
            return {"type": "alert", "message": result.get("message")}
        elif isinstance(result, list):
            # (should not be possible but allows for future changing)
            return {"type": "data", "rows": result}
        else:
            # General bug catch-all (should not be possible but just in case)
            return {"type": "error", "message": "Unexpected return type from entity"}
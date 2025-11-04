from Request import Request

class UpdateReqCont:
    def __init__(self):
        self.reqEntity = Request()

    def updateReqCont(self, userID: str):
        result = self.reqEntity.updateReq(userID)
        
        if isinstance(result, dict):
            return {"type": "error", "message": result.get("message")}
        elif isinstance(result, list):
            # (should not be possible but allows for future changing)
            return {"type": "data", "rows": result}
        else:
            # General bug catch-all (should not be possible but just in case)
            return {"type": "error", "message": "Unexpected return type from entity"}
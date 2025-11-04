from Request import Request

class ViewReqCont:
    def __init__(self):
        self.reqEntity = Request()

    def viewReqCont(self, userID: str):
        result = self.reqEntity.viewReq(userID)
        
        if isinstance(result, dict):
            return {"type": "error", "message": result.get("message")}
        elif isinstance(result, list):
            # (should not be possible but allows for future changing)
            return {"type": "data", "rows": result}
        else:
            # General bug catch-all (should not be possible but just in case)
            return {"type": "error", "message": "Unexpected return type from entity"}
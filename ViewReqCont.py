from Request import Request

class ViewReqCont:
    def __init__(self):
        self.reqEntity = Request()

    def viewReq(self, userID: str):
        result = self.reqEntity.viewReq(userID)
        
        if isinstance(result, dict):
            return {"type": "alert", "message": result.get("message")}
        elif isinstance(result, list):
            return {"type": "data", "rows": result}
        else:
            # General bug catch-all (should not be possible but just in case)
            return {"type": "error", "message": "Unexpected return type from entity"}
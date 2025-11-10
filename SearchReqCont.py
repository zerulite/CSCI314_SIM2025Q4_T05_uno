from Request import Request

class SearchReqCont:
    def __init__(self):
        self.reqEntity = Request()

    def searchReq(self, **kwargs):
        result = self.reqEntity.searchReq(**kwargs)

        if isinstance(result, dict):
            return {"type": "alert", "message": result.get("message")}
        elif isinstance(result, list):
            return {"type": "data", "rows": result}
        else:
            # General bug catch-all (should not be possible but just in case)
            return {"type": "error", "message": "Unexpected return type from entity"}
from Request import Request

class GenerateDailyReport:
    def __init__(self):
        self.entity = Request()

    def generateDailyReport(self, date):
        return self.entity.generateDailyReport(date)

from Request import Request

class GenerateWeeklyReport:
    def __init__(self):
        self.entity = Request()

    def generateWeeklyReport(self, week_start):
        return self.entity.generateWeeklyReport(week_start)

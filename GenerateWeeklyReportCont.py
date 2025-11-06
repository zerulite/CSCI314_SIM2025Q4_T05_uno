from Request import Request

class GenerateWeeklyReport:
    def __init__(self):
        self.entity = Request()

    def generate_weekly_report(self, week_start):
        return self.entity.get_requests_by_week(week_start)

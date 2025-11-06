from Request import Request

class GenerateDailyReport:
    def __init__(self):
        self.entity = Request()

    def generate_daily_report(self, date):
        return self.entity.get_requests_by_date(date)

from Request import Request

class GenerateMonthlyReport:
    def __init__(self):
        self.entity = Request()

    def generate_monthly_report(self, date):
        return self.entity.get_requests_by_month(date)

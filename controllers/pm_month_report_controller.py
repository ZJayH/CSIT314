from entities.report_entity import ReportEntity
from io import BytesIO

class PmMonthReportController:
    def handle_monthly(self, month_str: str = None) -> BytesIO:
        return ReportEntity.generate_monthly_report(month_str)

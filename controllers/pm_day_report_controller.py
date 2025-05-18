from entities.report_entity import ReportEntity
from io import BytesIO

class PmDayReportController:
    def handle_daily(self, date_str: str = None) -> BytesIO:
        return ReportEntity.generate_daily_report(date_str)

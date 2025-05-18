from entities.report_entity import ReportEntity
from io import BytesIO

class PmWeekReportController:
     def handle_weekly(self, week_start_str: str = None) -> BytesIO:
        return ReportEntity.generate_weekly_report(week_start_str)

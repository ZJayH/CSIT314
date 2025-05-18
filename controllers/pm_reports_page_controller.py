from entities.report_entity import ReportEntity
import pandas as pd


class ReportsPageController:
   def handle(self) -> dict:
        df = ReportEntity._base_df()
        df['date'] = pd.to_datetime(df['date'])

        dates = df['date'].dt.strftime('%Y-%m-%d').tolist()

        week_start = df['date'] - pd.to_timedelta(df['date'].dt.weekday, unit='D')
        weeks = sorted(week_start.dt.strftime('%Y-%m-%d').unique())

        months = sorted(df['date'].dt.strftime('%Y-%m').unique())

        return {
            'dates':  dates,
            'weeks':  weeks,
            'months': months,
        }
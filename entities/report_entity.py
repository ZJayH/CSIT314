import pandas as pd
from io import BytesIO
from datetime import datetime, timedelta
from sqlalchemy import func
from extensions import db
from .confirmed_matches_entity import ConfirmedMatchEntity

class ReportEntity:
    @staticmethod
    def _write_df_to_excel(df: pd.DataFrame, sheet_name: str) -> BytesIO:
        out = BytesIO()
        with pd.ExcelWriter(out, engine='xlsxwriter') as writer:
            df.to_excel(writer, index=False, sheet_name=sheet_name)
        out.seek(0)
        return out

    @classmethod
    def generate_daily_report(cls, date_str: str = None) -> BytesIO:
        # 1) determine target date
        if date_str:
            target = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            max_dt = db.session.query(func.max(ConfirmedMatchEntity.confirmed_date)).scalar()
            target = (max_dt.date() if max_dt else datetime.utcnow().date())

        # 2) count matches on that date
        count = (
            db.session.query(func.count(ConfirmedMatchEntity.match_id))
                      .filter(func.date(ConfirmedMatchEntity.confirmed_date) == target)
                      .scalar()
        )

        # 3) build one‐row DataFrame
        df = pd.DataFrame({'No. of Service Provided': [count]})
        return cls._write_df_to_excel(df, 'DailyReport')

    @classmethod
    def generate_weekly_report(cls, week_start_str: str = None) -> BytesIO:
        # 1) determine week start date (Monday)
        if week_start_str:
            ws = datetime.strptime(week_start_str, '%Y-%m-%d').date()
        else:
            max_dt = db.session.query(func.max(ConfirmedMatchEntity.confirmed_date)).scalar()
            latest = (max_dt.date() if max_dt else datetime.utcnow().date())
            ws = latest - timedelta(days=latest.weekday())

        # 2) count matches between ws and ws+6 days
        start = datetime.combine(ws, datetime.min.time())
        end   = start + timedelta(days=6, hours=23, minutes=59, seconds=59)
        count = (
            db.session.query(func.count(ConfirmedMatchEntity.match_id))
                      .filter(ConfirmedMatchEntity.confirmed_date >= start)
                      .filter(ConfirmedMatchEntity.confirmed_date <= end)
                      .scalar()
        )

        df = pd.DataFrame({
            'Week Start': [ws],
            'No. of Service Provided': [count]
        })
        return cls._write_df_to_excel(df, 'WeeklyReport')

    @classmethod
    def generate_monthly_report(cls, month_str: str = None) -> BytesIO:
        # 1) determine year & month
        if month_str:
            year, month = map(int, month_str.split('-'))
        else:
            max_dt = db.session.query(func.max(ConfirmedMatchEntity.confirmed_date)).scalar()
            latest = (max_dt.date() if max_dt else datetime.utcnow().date())
            year, month = latest.year, latest.month

        # 2) build start/end for the month
        start = datetime(year, month, 1)
        if month == 12:
            nxt = datetime(year+1, 1, 1)
        else:
            nxt = datetime(year, month+1, 1)
        end = nxt - timedelta(seconds=1)

        count = (
            db.session.query(func.count(ConfirmedMatchEntity.match_id))
                      .filter(ConfirmedMatchEntity.confirmed_date >= start)
                      .filter(ConfirmedMatchEntity.confirmed_date <= end)
                      .scalar()
        )

        df = pd.DataFrame({
            'Year-Month': [f"{year:04d}-{month:02d}"],
            'No. of Service Provided': [count]
        })
        return cls._write_df_to_excel(df, 'MonthlyReport')

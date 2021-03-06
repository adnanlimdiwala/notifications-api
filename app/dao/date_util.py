from datetime import datetime, timedelta

import pytz

from app.utils import convert_bst_to_utc


def get_months_for_financial_year(year):
    return [
        convert_bst_to_utc(month) for month in (
            get_months_for_year(4, 13, year) +
            get_months_for_year(1, 4, year + 1)
        )
        if month < datetime.now()
    ]


def get_months_for_year(start, end, year):
    return [datetime(year, month, 1) for month in range(start, end)]


def get_financial_year(year):
    return get_april_fools(year), get_april_fools(year + 1) - timedelta(microseconds=1)


def get_april_fools(year):
    """
     This function converts the start of the financial year April 1, 00:00 as BST (British Standard Time) to UTC,
     the tzinfo is lastly removed from the datetime becasue the database stores the timestamps without timezone.
     :param year: the year to calculate the April 1, 00:00 BST for
     :return: the datetime of April 1 for the given year, for example 2016 = 2016-03-31 23:00:00
    """
    return pytz.timezone('Europe/London').localize(datetime(year, 4, 1, 0, 0, 0)).astimezone(pytz.UTC).replace(
        tzinfo=None)


def get_month_start_and_end_date_in_utc(month_year):
    """
     This function return the start and date of the month_year as UTC,
     :param month_year: the datetime to calculate the start and end date for that month
     :return: start_date, end_date, month
    """
    import calendar
    _, num_days = calendar.monthrange(month_year.year, month_year.month)
    first_day = datetime(month_year.year, month_year.month, 1, 0, 0, 0)
    last_day = datetime(month_year.year, month_year.month, num_days, 23, 59, 59, 99999)
    return convert_bst_to_utc(first_day), convert_bst_to_utc(last_day)

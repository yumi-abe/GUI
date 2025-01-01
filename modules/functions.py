from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import List, Optional, Dict, Union

# strからdate型に変換する
def strToDate(date_input:Union[str, date]) -> date:
    if isinstance(date_input, str):
        toDate = datetime.strptime(date_input, "%Y/%m/%d").date()
    else:
        toDate = date_input
    return toDate

# strを入れたらdateに変換しつつ、日数差を計算する
def diff_days(start:Union[str, date], end:Union[str, date]) -> int:
    start = strToDate(start)
    end = strToDate(end)
    delta = end - start
    return delta.days
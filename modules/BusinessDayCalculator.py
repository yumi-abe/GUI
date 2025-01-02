import math
from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import List, Optional, Dict, Union

"""
〇営業日の日数を計算する
"""

class BusinessDayCalculator:
    def __init__(self, closed_days: List[date]):
        """
        :param closed_days: 休業日（祝日や特別な非営業日）のリスト
        例）
        closed_days = [
            date(2024, 1, 1),
            date(2024, 5, 3),
            date(2024, 12, 31),
        ]
        """
        self.closed_days = set(closed_days)

    def last_business_day(self, month:int, year:Optional[int]=None) -> date:
        """
        指定した月の月末営業日を計算
        :param month: 月（1～12）
        :param year: 年（Noneの場合は現在の年とする）
        :return : 月末営業日
        """
        if year == None:
            year = datetime.now().year

        if month == 12:
            month = 1
            year += 1
        else:
            month += 1

        #翌月月初の日付
        beginning = date(year, month, 1)
        #月初-1で当月末
        end = beginning - relativedelta(days=1)

        #当月末が土日または休業日の場合は平日になるまで日数を引く（＝月末営業日）
        while end.weekday() >= 5 or end in self.closed_days:
            end -= timedelta(days=1)
        
        return end
    
    def add_business_days(self, start_date:date, number_of_days:Optional[int]=2) -> date:
        """
        指定した日付から指定した日数の営業日を加算する
        :param start_date: 開始日
        :param number_of_days: 日数（初期値2日）
        :return: 加算後の日付（初期値の場合:2営業日後）
        """

        while number_of_days > 0:
            start_date += relativedelta(days=1)
            if start_date.weekday() < 5 and start_date not in self.closed_days:
                number_of_days -= 1
            
        return start_date
    
    def subtract_business_days(self, start_date:date, number_of_days:Optional[int]=2) -> date:
        """
        指定した日付から指定した日数の営業日を減算する
        :param start_date: 開始日
        :param number_of_days: 日数（初期値2日）
        :return: 減算後の日付（初期値の場合:2営業日前）
        """

        while number_of_days > 0:
            start_date -= relativedelta(days=1)
            if start_date.weekday() < 5 and start_date not in self.closed_days:
                number_of_days -= 1
        return start_date

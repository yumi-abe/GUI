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
    
    # def culculate_cross_trade(self, month:int, year:Optional[int]=None) -> Dict[str, date]:
    #     """
    #     クロス取引の日付を計算する
    #     :param month:対象月
    #     :param year:対象年（Noneの場合は今年）
    #     :return: クロス取引の各日付{権利確定日、権利付き最終日、権利落ち日}(dict形式)
    #     """
    #     cross_day = {}

    #     # 権利確定日
    #     last_date = self.last_business_day(month, year)
    #     cross_day["last_date"] = last_date

    #     # 権利付き最終日
    #     get_date = self.subtract_business_days(last_date)
    #     cross_day["get_date"] = get_date

    #     # 権利落ち日
    #     ex_date = self.add_business_days(get_date, 1)
    #     cross_day["ex_date"] = ex_date

    #     return cross_day



# from Get_DBdata import Get_DBdata

# get_DBdata = Get_DBdata()

# closed_days = get_DBdata.get_closed_days()


# stock_info = get_DBdata.get_stock_name()

# calculator = BusinessDayCalculator(closed_days)

# last_day = calculator.last_business_day(4, 2025)

# add_day = calculator.add_business_days(last_day)

# subtract_day = calculator.subtract_business_days(last_day)

# cross_day = calculator.culculate_cross_trade(4, 2025)

# def strToDate(date_input:Union[str, date]) -> date:
#     if isinstance(date_input, str):
#         toDate = datetime.strptime(date_input, "%Y/%m/%d").date()
#     else:
#         toDate = date_input
#     return toDate

# def diff_days(start:Union[str, date], end:Union[str, date]) -> int:
#     start = strToDate(start)
#     end = strToDate(end)
#     delta = end - start
#     return delta.days

# def calculate_cross_fee(amount:Union[str, int], quantity:Union[str, int], delta:int) -> Dict[str, int]:
#     cross_fee = {}
#     amount = float(amount) if isinstance(amount, str or int) else amount
#     quantity = int(quantity) if isinstance(quantity, str) else quantity
#     buy_fee = amount * quantity *  0.025 * 0.0027397 * 1
#     cross_fee['buy_fee'] = math.ceil(buy_fee)
#     sell_fee = amount * quantity * 0.014 * 0.0027397 * delta
#     cross_fee['sell_fee'] = math.ceil(sell_fee)
#     total_fee = buy_fee + sell_fee
#     cross_fee['total_fee'] = math.ceil(total_fee)

#     return cross_fee

# # toDate = strToDate('2025/04/30')
# # datetime_date = strToDate(toDate)
# # print(type(datetime_date))

# delta = diff_days(subtract_day, add_day)
# cross_fee = calculate_cross_fee(1000, 100, delta)
# print(cross_fee)

#    # 日数差計算（金利発生日数）
#     delta = end_date_object - start_date_object

#     delta_label.config(text=f"日数: {delta.days}日")

#     amount = float(amount_input.get())
#     quantity = int(quantity_input.get())

#     buy_fee = amount * quantity *  0.025 * 0.0027397 * 1
#     sell_fee = amount * quantity * 0.014 * 0.0027397 * delta.days
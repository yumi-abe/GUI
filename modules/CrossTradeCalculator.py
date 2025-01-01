from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta
from typing import List, Optional, Dict, Union
import math
from modules.BusinessDayCalculator import BusinessDayCalculator
from modules.functions import strToDate, diff_days

"""
クロス取引の日程や手数料を計算する
（BusinessDayCalculatorの子クラス）
"""
class CrossTradeCaluculator(BusinessDayCalculator):
    def __init__(self, closed_days: List[date], amount: Union[str, int], quantity: Union[str, int]):
        """
        :param closed_days: 休業日（祝日や特別な非営業日）のリスト
        :param amount: 金額（株価）
        :param quantity: 数量（株数）
        """
        super().__init__(closed_days) # 親クラスの初期化
        self.amount = amount
        self.quantity = quantity

    
    def culculate_cross_trade(self, month:int, start:Union[str, date], year:Optional[int]=None) -> Dict[str, date]:
        """
        クロス取引の日付を計算する
        :param month:対象月
        :param start:取得日
        :param year:対象年（Noneの場合は今年）
        :return: クロス取引の各日付{権利確定日、権利付き最終日、権利落ち日}(dict形式)
        """
        cross_day = {}

        # クロス受け渡し日（約定日の2営業日後）
        start = strToDate(start)
        start_date = self.add_business_days(start)
        cross_day['start_date'] = start_date

        # 権利確定日(決算月の月末営業日)
        confirmed_date = self.last_business_day(month, year)
        cross_day["confirmed_date"] = confirmed_date

        # 権利付き最終日（権利確定日の2営業日前）
        get_date = self.subtract_business_days(confirmed_date)
        cross_day["get_date"] = get_date

        # 権利落ち日（権利月最終日の1営業日後）
        ex_date = self.add_business_days(get_date, 1)
        cross_day["ex_date"] = ex_date

        #現渡受け渡し日(権利落ち日の2営業日後)
        transaction_date = self.add_business_days(ex_date)
        cross_day["transaction_date"] = transaction_date


        return cross_day
    
    def calculate_cross_fee(self, month:int, start:Union[str, date], end:Optional[Union[str, date]]=None) -> Dict[str, int]:
        """
        クロス取引の手数料計算
        :param start:開始日（取得日）
        :param end:終了日
        :return: 手数料{信用買手数料、信用売手数料、合計（信用売＋信用買）}
        """

        cross_day = self.culculate_cross_trade(month, start)
        # 現渡受け渡し日
        if end == None:
            end = cross_day['transaction_date']
    
        cross_fee = {}

        delta = diff_days(start, end)
        cross_fee['delta'] = delta
        amount = self.amount
        quantity = self.quantity

        amount = float(amount) if isinstance(amount, str or int) else amount
        quantity = int(quantity) if isinstance(quantity, str) else quantity
        buy_fee = amount * quantity *  0.025 * 0.0027397 * 1
        cross_fee['buy_fee'] = math.ceil(buy_fee)
        sell_fee = amount * quantity * 0.014 * 0.0027397 * delta
        cross_fee['sell_fee'] = math.ceil(sell_fee)
        total_fee = buy_fee + sell_fee
        cross_fee['total_fee'] = math.ceil(total_fee)

        return cross_fee



# from Get_DBdata import Get_DBdata

# get_DBdata = Get_DBdata()

# closed_days = get_DBdata.get_closed_days()


# stock_info = get_DBdata.get_stock_name(1444)



# caluculator = CrossTradeCaluculator(closed_days, amount=1000, quantity=100)

# cross_day = caluculator.culculate_cross_trade(12, "2024/12/20")
# print(cross_day)
# cross_fee = caluculator.calculate_cross_fee("2024/12/2", "2024/12/20")
# print(cross_fee)
# last = caluculator.last_business_day(11, 2024)
# print(last)
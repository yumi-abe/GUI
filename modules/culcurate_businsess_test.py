from datetime import date, timedelta, datetime
from dateutil.relativedelta import relativedelta



def culcurate_cross_day(month, closed_days, number_of_days=2):
    cross_day = {}

    # 権利確定日（月末営業日）の計算
    year = datetime.now().year
    if month == 12:
        month = 1
        year += 1
    else:
        month += 1

        # 翌月月初の日付
    beginning = date(year, month, 1)
        # 月初-1で当月末
    end = beginning - relativedelta(days=1)

        # 当月末が土日または休業日の場合は日数を-1にして平日になるまで引く（=月末営業日）
    while end.weekday() >= 5 or end in closed_days:
        end -= timedelta(days=1)
    last_date = end

    cross_day['last_date'] = last_date

    # 権利月付き最終日の計算
    while number_of_days > 0:
        last_date -= timedelta(days=1)
        if last_date.weekday() < 5 and last_date not in closed_days:
            number_of_days -= 1
    get_date = last_date
    cross_day['get_date'] = get_date

    # 権利落ち日の計算
    ex_date = last_date + timedelta(days=1)

    cross_day['ex_date'] = ex_date

    return cross_day


from modules.Get_DBdata import get_closed_days

# データベースから休業日取得
closed_days = get_closed_days('test')

cross_day = culcurate_cross_day(6, closed_days)

print(cross_day)

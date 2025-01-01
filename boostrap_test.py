import tkinter as tk
import ttkbootstrap as tb
from tkinter import messagebox
import holidays
from datetime import datetime, timedelta
import math


root = tb.Window(themename="superhero")

root.title("手数料計算")
root.geometry("500x1100+1700+50")

def show_message():
    api_name = "〇〇株式会社"
    api_amount = 100

    code_name.config(text=f"銘柄名: {api_name},株価:{api_amount}円")
    
    if api_amount > 0:
        amount_input.insert(0, api_amount)


def fee_culculation():

    # 文字列⇀日付変換
    def strToDate(date):
        toDate = datetime.strptime(date, "%Y/%m/%d")
        return toDate
    
    def add_business_days_with_holidays(start_date, business_days_to_add):
        current_date = start_date
        # 日本の祝日リストを取得
        jp_holidays = holidays.CountryHoliday('JP')
        
        while business_days_to_add > 0:
            current_date += timedelta(days=1)
            # 土日と祝日を除外
            if current_date.weekday() < 5 and current_date not in jp_holidays:
                business_days_to_add -= 1
        return current_date
    
    # ラベル表示
    start_label.config(text=f"選択日: {start_date.entry.get()}")
    end_label.config(text=f"終了日: {end_date.entry.get()}")

    # 日付の取得、date型に変換
    start = start_date.entry.get()
    start_date_object = strToDate(start)

    # test
    result_date = add_business_days_with_holidays(start_date_object, 2)
    print(result_date)

    end = end_date.entry.get()
    end_date_object = strToDate(end)

    # 日数差計算（金利発生日数）
    delta = end_date_object - start_date_object

    delta_label.config(text=f"日数: {delta.days}日")

    amount = float(amount_input.get())
    quantity = int(quantity_input.get())

    buy_fee = amount * quantity *  0.025 * 0.0027397 * 1
    sell_fee = amount * quantity * 0.014 * 0.0027397 * delta.days

    print(amount)
    print(math.ceil(buy_fee))
    print(math.ceil(sell_fee))





# 銘柄コード入力ボックス
tb.Label(root, text="銘柄コード(数字4桁)", bootstyle="success").pack(pady=10)
code = tb.Entry(root,bootstyle="success")
code.pack()

# 検索ボタン
code_button = tb.Button(root, text="検索", bootstyle="light", command=show_message)
code_button.pack(pady=10)

# 銘柄名表示ラベル
code_name = tb.Label(root, text="", bootstyle="light")
code_name.pack(pady=10)

# 株価入力ボックス
tb.Label(root, text="株価", bootstyle="success").pack(pady=(10,0))
amount_input = tb.Entry(root)
amount_input.pack(pady=10)

# 株数入力ボックス
tb.Label(root, text="株数", bootstyle="success").pack(pady=(10,0))
quantity_input = tb.Entry(root)
quantity_input.pack(pady=10)

# 取得日選択（カレンダー）
tb.Label(root, text="取得日", bootstyle="success").pack(pady=10)
start_date = tb.DateEntry(root, bootstyle="success")
start_date.pack(pady=(0,20))

# 権利確定日選択（カレンダー）
tb.Label(root, text="権利確定日", bootstyle="primary").pack(pady=(20,0))
end_date = tb.DateEntry(root, bootstyle="primary")
end_date.pack(pady=(0,40))

# 計算するボタン
date_button = tb.Button(root, text="計算する", bootstyle="success", command=fee_culculation)
date_button.pack(pady=20)

# ラベル表示
start_label = tb.Label(root, text="取得日: ")
start_label.pack(pady=20)

end_label = tb.Label(root, text="権利確定日: ")
end_label.pack(pady=20)

delta_label = tb.Label(root, text="金利発生日数: ")
delta_label.pack(pady=20)

fee_label = tb.Label(root, text="手数料: ")
fee_label.pack(pady=20)












root.mainloop()

from datetime import datetime
import tkinter as tk
import tkinter.messagebox as messagebox
import ttkbootstrap as tb
from modules.Get_DBdata import Get_DBdata
from modules.stock_search import stock_search
from modules.CrossTradeCalculator import CrossTradeCaluculator
from modules.functions import strToDate

class StockAPP:
    def __init__(self, root):
        """初期化"""
        self.root = root
        self.root.title("手数料計算")
        self.root.geometry("700x1100+1000+50")

        # 銘柄コード入力ボックス
        tb.Label(root, text="銘柄コード(数字4桁)", bootstyle="success").pack(pady=10)
        self.code = tb.Entry(root,bootstyle="success")
        self.code.pack()

        # 検索ボタン
        self.code_button = tb.Button(root, text="検索", bootstyle="light", command=self.show_stock_name)
        self.code_button.pack(pady=10)

        # 銘柄名表示ラベル
        self.code_name = tb.Label(root, text="", bootstyle="light")
        self.code_name.pack()

        frame = tb.Frame(root)
        frame.pack(pady=10)

        # 株価入力ラベル（検索した場合は結果表示）
        tb.Label(frame, text='株価', bootstyle="success").grid(row=0, column=0, padx=10)
        self.amount = tb.Entry(frame, bootstyle="success")
        self.amount.grid(row=1, column=0, padx=10)

        # 株数入力ボックス
        tb.Label(frame, text="株数", bootstyle="success").grid(row=0, column=1)
        self.quantity = tb.Combobox(frame, values=[str(i) for i in range(100, 1001, 100)], state="readonly")
        self.quantity.current(0)
        self.quantity.grid(row=1, column=1)

        # 取得日（カレンダー）
        tb.Label(frame, text="取得日", bootstyle="success").grid(row=2, column=0, padx=30, pady=10)
        self.get_date = tb.DateEntry(frame, bootstyle="success")
        self.get_date.grid(row=3, column=0, padx=30)

        # 優待月
        tb.Label(frame, text="優待月", bootstyle="success").grid(row=2, column=1, pady=10)
        self.select_month = tb.Combobox(frame, values=[f"{i}月" for i in range(1,13)], state="readonly", bootstyle="success")
        current_month = datetime.now().month
        self.select_month.set(f"{current_month}月")
        self.select_month.grid(row=3, column=1)
        
        # 計算ボタン
        self.culculate_button = tb.Button(root, text="手数料計算", bootstyle="light", command=self.calculate)
        self.culculate_button.pack(pady=20)

        # 日数コメントラベル
        self.date_result = tb.Label(root, text="", bootstyle="light")
        self.date_result.pack(pady=10)

        # 手数料コメントラベル
        self.fee_result = tb.Label(root, text="", bootstyle="light")
        self.fee_result.pack(pady=10)

        # 合計コメントラベル
        self.total_result = tb.Label(root, text="", bootstyle="light")
        self.total_result.pack(pady=10)



    def clear_results(self):
        """
        ラベルを初期化
        """
        self.date_result.config(text="")
        self.fee_result.config(text="")
        self.total_result.config(text="")


    def show_stock_name(self):
        """
        検索ボタンを押すと銘柄名、株価を表示する
        """
        stock_code = self.code.get()
        stock_info = stock_search(stock_code) #yfで銘柄検索

        # 見つからなかった場合はメッセージを表示
        if isinstance(stock_info, str):
            self.code_name.config(text=stock_info)
            self.amount.delete(0, 'end') #金額を初期化
            self.clear_results() #ラベルを初期化
        else:
            # 銘柄名、株価を表示
            stock_price = stock_info['stock_price']
            formated_price = "{:,}".format(stock_price)
            self.code_name.config(text=f"銘柄名: {stock_info['stock_name']}  株価:{formated_price}円")
            # 株価が存在する場合は金額欄に株価を入力
            if stock_price > 0:
                self.amount.delete(0, 'end')  # 既存の値をクリア
                self.amount.insert(0, stock_price)  # 株価を挿入
                self.clear_results() #ラベルを初期化

    def calculate(self):
        """
        計算結果の表示
        """
        amount = self.amount.get()
        quantity = self.quantity.get()
        month = self.select_month.get()
        get_date = self.get_date.entry.get()

        # 未入力の場合はエラーメッセージを表示
        if not amount or not quantity or not month or not get_date:
            messagebox.showerror("エラー","金額、株数、優待月、取得日は必須です。")
            return

        month = int(month.replace('月', ''))
        date = strToDate(get_date)

        # 休業日取得
        get_DBdata = Get_DBdata()
        closed_days = get_DBdata.get_closed_days()

        # 手数料計算クラス呼び出し
        calculator = CrossTradeCaluculator(closed_days,amount, quantity)
        # クロス取引日程計算
        cross_day = calculator.culculate_cross_trade(month, date)
        # クロス取引手数料計算
        cross_fee = calculator.calculate_cross_fee(month, cross_day['start_date'])
        fomat_get_date = cross_day['get_date'].strftime("%Y年%m月%d日")
        # 結果をラベルで表示
        self.date_result.config(text=f"権利付最終日: {fomat_get_date}  金利発生日数:{cross_fee['delta']}日")
        self.fee_result.config(text=f"買建金利: {cross_fee['buy_fee']}円 売建金利: {cross_fee['sell_fee']}円")
        self.total_result.config(text=f"手数料合計: {cross_fee['total_fee']}円")
    


if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = StockAPP(root)
    root.mainloop()




import tkinter as tk
import ttkbootstrap as tb
from modules.Get_DBdata import Get_DBdata
from modules.stock_search import stock_search


class StockAPP:
    def __init__(self, root):
        """初期化"""
        self.root = root
        self.root.title("手数料計算")
        self.root.geometry("500x1100+1300+50")

        # 銘柄コード入力ボックス
        tb.Label(root, text="銘柄コード(数字4桁)", bootstyle="success").pack(pady=10)
        self.code = tb.Entry(root,bootstyle="success")
        self.code.pack()

        # 検索ボタン
        self.code_button = tb.Button(root, text="検索", bootstyle="light", command=self.show_message)
        self.code_button.pack(pady=10)

        # 銘柄名表示ラベル
        self.code_name = tb.Label(root, text="", bootstyle="light")
        self.code_name.pack(pady=10)

        tb.Label(root, text='株価', bootstyle="success").pack(pady=10)
        self.amount = tb.Entry(root, bootstyle="success")
        self.amount.pack()
        

    def show_message(self):
        """
        検索ボタンを押すと銘柄名、株価を表示する
        """
        stock_code = self.code.get()
        stock_info = stock_search(stock_code)

        # 見つからなかった場合はメッセージを表示
        if isinstance(stock_info, str):
            self.code_name.config(text=stock_info)
            self.amount.delete(0, 'end')
        else:
            # 銘柄名、株価を表示
            stock_price = stock_info['stock_price']
            formated_price = "{:,}".format(stock_price)
            self.code_name.config(text=f"銘柄名: {stock_info['stock_name']}  株価:{formated_price}円")
            # 株価が存在する場合は金額欄に株価を入力
            if stock_price > 0:
                self.amount.delete(0, 'end')  # 既存の値をクリア
                self.amount.insert(0, formated_price)  # 株価を挿入


if __name__ == "__main__":
    root = tb.Window(themename="superhero")
    app = StockAPP(root)
    root.mainloop()


# def show_message():
#     """
#     検索ボタンを押すと銘柄名、株価を表示する
#     """
#     stock_code = code.get()
#     stock_info = stock_search(stock_code)

#     # 見つからなかった場合はメッセージを表示
#     if isinstance(stock_info, str):
#         code_name.config(text=stock_info)
#         amount.delete(0, 'end')
#         return
    
#     # 銘柄名、株価を表示
#     stock_price = stock_info['stock_price']
#     formated_price = "{:,}".format(stock_price)
#     code_name.config(text=f"銘柄名: {stock_info['stock_name']}  株価:{formated_price}円")
#     # 株価が存在する場合は金額欄に株価を入力
#     if stock_price > 0:
#         amount.delete(0, 'end')  # 既存の値をクリア
#         amount.insert(0, formated_price)  # 株価を挿入








# root = tb.Window(themename="superhero")

# root.title("手数料計算")
# root.geometry("500x1100+1300+50")

# # 銘柄コード入力ボックス
# tb.Label(root, text="銘柄コード(数字4桁)", bootstyle="success").pack(pady=10)
# code = tb.Entry(root,bootstyle="success")
# code.pack()

# # 検索ボタン
# code_button = tb.Button(root, text="検索", bootstyle="light", command=show_message)
# code_button.pack(pady=10)

# # 銘柄名表示ラベル
# code_name = tb.Label(root, text="", bootstyle="light")
# code_name.pack(pady=10)

# tb.Label(root, text='株価', bootstyle="success").pack(pady=10)
# amount = tb.Entry(root, bootstyle="success")
# amount.pack()





# root.mainloop()





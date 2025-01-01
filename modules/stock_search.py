import os
import sys
import pandas as pd
import yfinance as yf

from modules.Get_DBdata import Get_DBdata

"""
入力されたコードに該当する銘柄情報を取得
"""

def stock_search(code):

    stock_code = f"{code}.T"

    stock = yf.Ticker(stock_code)
    # if stock == None:
    #     result = "該当の銘柄は見つかりませんでした。"
    # else:
    try:
        data = stock.history(period="1d")
        if data.empty:
            return "該当の銘柄は見つかりませんでした。"
        
        price = round(data['Close'].iloc[0])
        get_DBdata = Get_DBdata()
        stock_name = get_DBdata.get_stock_name(code)

        result = {
            'code': code,
            'stock_name': stock_name,
            'stock_price': price
        }
    except Exception as e:
        result = f"エラーが発生しました: {e}"

    return result

# stock = stock_search(1234)
# print(stock)






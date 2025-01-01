import os
import pandas as pd
import requests
import sqlite3
import time

from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from typing import Optional

"""
スクレイピングして各種データを取得するためのclass
"""

class DataFetcher:
    def __init__(self, dbname:Optional[str]='test.db'):
        self.dbname = dbname
    
    def _setup_diver(self):
        """WebDriverのセットアップ"""
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=chrome_options)

    def connect_db(self):
        """データベースに接続"""
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def create_table(self, table_sql:str):
        """テーブルを作成するための共通メソッド"""
        self.cursor.execute(table_sql)
        self.conn.commit()

    def get_table_data(self, table_name:str, sql:Optional[str]=None):
        """テーブル情報取得"""
        if sql == None:
            sql = f"SELECT * FROM {table_name}"
        
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows

    def get_calendar(self):
        """JPXカレンダー情報を取得する"""
        # スクレイピング
        self._setup_diver()
        self.driver.get("https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html")
        self.driver.implicitly_wait(5)

        # 休業日部分を取得してカレンダー配列に格納
        calendar = []
        elemets = self.driver.find_elements(By.XPATH, "//tr/td[1]")
        for element in elemets:
            date = element.text.split('（')[0] #（曜日）を切り離す
            date = datetime.strptime(date, '%Y/%m/%d') #datetime型へ
            calendar.append(date.date())
        
        self.driver.quit()

        # データベースへ登録
        self.connect_db()
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()
        sql = """CREATE TABLE IF NOT EXISTS calendar (id INTEGER PRIMARY KEY, date TEXT);"""
        self.create_table(sql)

        try:
            for date in calendar:
                self.cursor.execute("INSERT INTO test (date) values (?)", (date.isoformat(),))
            # commit（保存）
            self.conn.commit()
            print("データを挿入しました")
        except sqlite3.Error as e:
            print(f"エラー: {e}")
        finally:
            rows = self.get_table_data('calendar')
            closed_days = []
            for row in rows:
                date = datetime.strptime(row[1], "%Y-%m-%d").date()
                closed_days.append(date)
            # 接続を閉じる
            self.conn.close()
        return calendar
    
    def get_stock_info(self):
        """JPXの株式名情報を取得してデータベースに保存"""
        self._setup_diver()
        self.driver.get("https://www.jpx.co.jp/markets/statistics-equities/misc/01.html")
        self.driver.implicitly_wait(5)

        # エクセルファイルURL取得
        link = self.driver.find_element(By.XPATH, '//td//a[contains(@href, ".xls")]')
        file_url = link.get_attribute('href')

        # ファイルを保存
        save_dir = "./files"
        file_path = os.path.join(save_dir, "stock_name.xls")
        os.makedirs(save_dir, exist_ok=True)

        # ファイルをダウンロード
        response = requests.get(file_url)
        with open(file_path, 'wb') as f:
            f.write(response.content)

        self.driver.quit()

         # データベース接続
        self.connect_db()
        sql = """
        CREATE TABLE IF NOT EXISTS stock_info (
            code CHAR(4) PRIMARY KEY,
            name TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.create_table(sql)

        try:
            df = pd.read_excel(file_path)
            for data in zip(df['コード'], df['銘柄名']):
                self.cursor.execute('''
                INSERT OR REPLACE INTO stock_info (code, name) VALUES (?, ?)
                ''', (data[0], data[1]))
            self.conn.commit()
            print("株式名のデータを挿入しました")
        except sqlite3.Error as e:
            print(f"エラー: {e}")
        finally:
            rows = self.get_table_data('stock_info')
            stock_info = []
            for row in rows:
                stock_info.append({
                    'code': row[0],
                    'stock_name': row[1]
                })

            # 接続を閉じる
            self.conn.close()
        return stock_info


fetcher = DataFetcher()




stock_info = fetcher.get_stock_info()

print(stock_info)

calendar = fetcher.get_calendar()
print(calendar)


# def get_calendar():

#     # Chromeのオプション設定
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # ヘッドレスモード（GUIなしで実行）

#     driver = webdriver.Chrome(options=chrome_options)

#     driver.get("https://www.jpx.co.jp/corporate/about-jpx/calendar/index.html")

#     # ページタイトルを表示
#     title = driver.title

#     # # ページが完全に読み込まれるまで待機
#     # time.sleep(5)  # 必要に応じて調整
#     driver.implicitly_wait(5)

#     calendar = []
#     elements = driver.find_elements(By.XPATH, "//tr/td[1]")  # 1番目の<td>を指定
#     for element in elements:
#         date = element.text.split('（')[0] #（曜日）を切り離す
#         date = datetime.strptime(date, '%Y/%m/%d') #datetime型へ
#         calendar.append(date.date())
#     # print(calendar)

#     # WebDriverを終了
#     driver.quit()



#     # データベース接続
#     dbname = ('test.db')
#     conn = sqlite3.connect(dbname)

#     cursor = conn.cursor()

#     sql = """CREATE TABLE IF NOT EXISTS test(
#                 id INTEGER PRIMARY KEY,
#                 date TEXT
#                 )"""

#     # SQL文実行
#     cursor.execute(sql)

#     try:
#         for date in calendar:
#             cursor.execute("INSERT INTO test (date) values (?)", (date.isoformat(),))
#         # commit（保存）
#         conn.commit()
#         print("データを挿入しました")
#     except sqlite3.Error as e:
#         print(f"エラー: {e}")
#     finally:
#         # 接続を閉じる
#         conn.close()


# def get_stock_name():
#     # Chromeのオプション設定
#     chrome_options = Options()
#     chrome_options.add_argument("--headless")  # ヘッドレスモード（GUIなしで実行）

#     driver = webdriver.Chrome(options=chrome_options)

#     driver.get("https://www.jpx.co.jp/markets/statistics-equities/misc/01.html")

#     driver.implicitly_wait(5)

#     link = driver.find_element(By.XPATH, '//td//a[contains(@href, ".xls")]')
#     file_url = link.get_attribute('href')

#     save_dir = "./files"
#     file_path = os.path.join(save_dir, "stock_name.xls")

#     os.makedirs(save_dir, exist_ok=True)

#     response = requests.get(file_url)
#     with open(file_path, 'wb') as f:
#         f.write(response.content)

#     # WebDriverを終了
#     driver.quit()


#     # データベース接続
#     dbname = ('test.db')
#     conn = sqlite3.connect(dbname)

#     cursor = conn.cursor()

#     sql = """
#     CREATE TABLE IF NOT EXISTS stock_info (
#         code CHAR(4) PRIMARY KEY,
#         name TEXT NOT NULL,
#         created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
#     );
#     """

#     # SQL文実行
#     cursor.execute(sql)


#     try:
#         df = pd.read_excel(file_path)
#         for data in zip(df['コード'], df['銘柄名']):
#             cursor.execute('''
#             INSERT OR REPLACE INTO stock_info (code, name) VALUES (?, ?)
#             ''', (data[0], data[1]))

#             # 変更をコミット（保存）
#         conn.commit()

#         print("データを挿入しました")
#     except sqlite3.Error as e:
#         print(f"エラー: {e}")
#     finally:
#         # 接続を閉じる
#         conn.close()


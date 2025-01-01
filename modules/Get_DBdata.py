import sqlite3
from datetime import datetime
from typing import Optional, List, Union

"""
データベースからのデータ取得関連
"""

class Get_DBdata():
    def __init__(self, dbname:Optional[str]='test.db'):
        self.dbname = dbname

    def connect_db(self):
        self.conn = sqlite3.connect(self.dbname)
        self.cursor = self.conn.cursor()

    def get_data(self, table_name:str, sql:Optional[str]=None):
        if sql == None:
            sql = f"SELECT * FROM {table_name}"
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()
        return rows
    
    def get_closed_days(self)-> List[datetime.date]:
        self.connect_db()
        rows = self.get_data('test')
        closed_days = []
        for row in rows:
            date = datetime.strptime(row[1], "%Y-%m-%d").date()
            closed_days.append(date)
        # 接続を閉じる
        self.conn.close()
        return closed_days

    def get_stock_list(self)-> dict[str, str]:
        self.connect_db()
        rows = self.get_data('stock_info')
        stock_info = []
        for row in rows:
            info = {
                    'code': row[0],
                    'stock_name': row[1]
            }
            stock_info.append(info)
        # 接続を閉じる
        self.conn.close()
        return stock_info
    
    def get_stock_name(self, code:Union[str, int])-> str:
        if isinstance(code, int):
            code = str(code)
        self.connect_db()
        rows = self.get_data('stock_info')
        stock_name = "なし"
        for item in rows:
            if item[0] == code:
                stock_name = item[1]
                break
        # 接続を閉じる
        self.conn.close()
        return stock_name

# get_DBdata = Get_DBdata()
# name = get_DBdata.get_stock_name(1429)
# print(name)

# closed_days = get_DBdata.get_closed_days()

# print(closed_days)

# stock_info = get_DBdata.get_stock_info()
# print(stock_info)

# def get_closed_days(table_name):

#     # データベース接続
#     dbname = ('test.db')
#     conn = sqlite3.connect(dbname)

#     cursor = conn.cursor()

#     sql = f"SELECT * FROM {table_name}"

#     # SQL文実行
#     cursor.execute(sql)

#     rows = cursor.fetchall()

#     closed_days = []
#     for row in rows:
#         date = datetime.strptime(row[1], "%Y-%m-%d").date()
#         closed_days.append(date)


#     # 接続を閉じる
#     conn.close()

#     return closed_days


# def get_stock_info(table_name):

#     # データベース接続
#     dbname = ('test.db')
#     conn = sqlite3.connect(dbname)

#     cursor = conn.cursor()

#     sql = f"SELECT * FROM {table_name}"

#     # SQL文実行
#     cursor.execute(sql)

#     rows = cursor.fetchall()
#     stock_info = {}
#     for row in rows:
#        stock_info = {
#             'code': row[0],
#             'stock_name': row[1]
#        }


#        print(stock_info)


#     # 接続を閉じる
#     conn.close()





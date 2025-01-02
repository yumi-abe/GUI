import sqlite3
from typing import Optional

class DatabaseManager:
    def __init__(self, dbname: Optional[str] = 'test.db'):
        self.dbname = dbname
        self.conn = None
        self.cursor = None

    def connect(self):
        """データベースに接続"""
        if self.conn is None:
            self.conn = sqlite3.connect(self.dbname)
            self.cursor = self.conn.cursor()

    def close(self):
        """接続を閉じる"""
        if self.conn:
            self.conn.close()
            self.conn = None
            self.cursor = None

    def execute(self, sql: str, params: Optional[tuple] = None):
        """SQLを実行"""
        self.connect()
        if params:
            self.cursor.execute(sql, params)
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()
    
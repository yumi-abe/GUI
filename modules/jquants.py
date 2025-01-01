import json

import pandas as pd
import requests
from dotenv import load_dotenv
import os
import csv
import sys

if len(sys.argv) > 2:
    start_date = sys.argv[1]
    end_date = sys.argv[2]
    print(f"開始日{start_date}")
    print(f"終了日{end_date}")
else:
    print("データがありません")

    
# 認証情報読み込み
load_dotenv()
MAIL_ADDRESS = os.environ["MAIL_ADDRESS"]
PASSWORD = os.environ["PASSWORD"]

resp = requests.post(
    "https://api.jquants.com/v1/token/auth_user",
    data=json.dumps({"mailaddress": MAIL_ADDRESS, "password": PASSWORD})
)
REFRESH_TOKEN = resp.json()["refreshToken"]

resp = requests.post(
    "https://api.jquants.com/v1/token/auth_refresh",
    params={"refreshtoken": REFRESH_TOKEN}
)
ID_TOKEN = resp.json()["idToken"]

url = f"https://api.jquants.com/v1/markets/trading_calendar?holidaydivision=1&from={start_date}&to={end_date}"

resp = requests.get(
    url,headers={"Authorization": f"Bearer {ID_TOKEN}"}
)
calendar = resp.json()

print(calendar)

file_name = "jquants.csv"

with open(file_name, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=["Date", "HolidayDivision"])
    writer.writeheader()
    writer.writerows(calendar['trading_calendar'])


print(f"{file_name}に書き込みしました")


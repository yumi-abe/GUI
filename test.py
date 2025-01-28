import requests
apiKey = 'KI3GYP4RKRO9MP4L'
STOCK = "TSLA"

params = {
    "function": "TIME_SERIES_INTRADAY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": apiKey,
}
url = "https://www.alphavantage.co/query" # エンドポイント
response = requests.get(url, params=params)
print(response.json())
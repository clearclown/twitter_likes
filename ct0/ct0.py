import requests

# Twitterの開発者ページのURL
url = "https://developer.twitter.com/en"

# セッションの作成
session = requests.Session()

# URLに対してGETリクエストを送信
response = session.get(url)

# レスポンスからct0クッキーを取得
ct0 = response.cookies.get('ct0')

# ct0トークンを表示
print(ct0)

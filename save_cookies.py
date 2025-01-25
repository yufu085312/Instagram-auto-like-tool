from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import time
import os


# クッキーを保存する関数
def save_cookies(username, password):
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(options=options)

    # Instagramのログインページにアクセス
    driver.get("https://www.instagram.com/accounts/login/")
    time.sleep(20)

    # ユーザー名とパスワードを入力
    driver.find_element(By.NAME, "username").send_keys(username)
    driver.find_element(By.NAME, "password").send_keys(password)
    driver.find_element(By.NAME, "password").send_keys(Keys.RETURN)

    time.sleep(5)  # ログイン完了を待つ

    # クッキーを取得して保存
    cookies = driver.get_cookies()

    # 保存先ディレクトリの確認と作成
    cookies_dir = "config/cookies/"
    os.makedirs(cookies_dir, exist_ok=True)

    # クッキーを保存
    with open(f"{cookies_dir}{username}_cookies.json", "w") as file:
        json.dump(cookies, file)

    print(f"クッキーが保存されました: {cookies_dir}{username}_cookies.json")
    driver.quit()

# メイン処理
if __name__ == "__main__":
    # アカウント情報の読み込み
    with open("config/accounts.json", "r") as file:
        accounts = json.load(file)

    # 各アカウントでログインしてクッキーを保存
    for account in accounts:
        username = account["username"]
        password = account["password"]
        print(f"{username} のクッキーを保存しています...")
        save_cookies(username, password)

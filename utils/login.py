import json
import os
import time

def login_with_cookies(driver, username):
    """
    クッキーを使って自動ログインを試みます。
    :param driver: Selenium WebDriver
    :param username: ユーザー名
    """
    cookies_file = f"config/cookies/{username}_cookies.json"
    try:
        if os.path.exists(cookies_file):
            print(f"クッキーをロード中: {cookies_file}")
            with open(cookies_file, "r") as file:
                cookies = json.load(file)
            driver.get("https://www.instagram.com/")
            for cookie in cookies:
                driver.add_cookie(cookie)
            driver.refresh()
            time.sleep(3)  # ページロード待機
            print(f"{username} のクッキーでログインしました")
        else:
            print(f"クッキーが存在しません: {cookies_file}")
            raise FileNotFoundError(f"{cookies_file} が存在しません")
    except Exception as e:
        print(f"クッキーのロード中にエラーが発生しました: {e}")
        raise

def save_cookies(driver, username):
    """
    現在のセッションからクッキーを保存します。
    """
    try:
        cookies = driver.get_cookies()
        cookies_dir = "config/cookies/"
        os.makedirs(cookies_dir, exist_ok=True)
        with open(f"{cookies_dir}{username}_cookies.json", "w") as file:
            json.dump(cookies, file)
        print(f"{username} のクッキーが保存されました: {cookies_dir}{username}_cookies.json")
    except Exception as e:
        print(f"クッキー保存中にエラーが発生しました: {e}")

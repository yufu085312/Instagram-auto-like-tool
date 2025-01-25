from selenium import webdriver
import json
import time

def login_with_cookies(driver, username):
    try:
        with open(f'config/cookies/{username}_cookies.json', 'r') as file:
            cookies = json.load(file)

        driver.get('https://www.instagram.com/')
        for cookie in cookies:
            driver.add_cookie(cookie)
        driver.refresh()
        time.sleep(3)
    except FileNotFoundError:
        print(f"{username} のクッキーが見つかりません。手動ログインしてください。")

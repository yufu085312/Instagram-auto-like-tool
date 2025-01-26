import logging
import json
import os
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.login import login_with_cookies, save_cookies
from utils.hashtag_search import search_hashtag, filter_recent_posts
from utils.post_interaction import interact_with_post
from utils.driver_setup import init_driver

# ログ設定
logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def process_accounts(accounts, hashtag, desired_username=None):
    """
    アカウントごとにログインと投稿処理を実行します。
    """
    for account in accounts:
        driver = init_driver()
        username = account['username']
        password = account.get('password')  # パスワードを取得（必要な場合に手動ログイン用）

        try:
            # クッキーを使用してログイン
            cookies_file = f"config/cookies/{username}_cookies.json"
            if not os.path.exists(cookies_file):
                print(f"クッキーが存在しません: {cookies_file}")
                print(f"{username} の手動ログインを行ってください...")
                driver.get("https://www.instagram.com/accounts/login/")
                time.sleep(100)  # 手動ログインの時間を与える
                save_cookies(driver, username)  # クッキーを保存

            logging.info(f"{username} でログインを試みます")
            print(f"{username} でログインを試みます")
            login_with_cookies(driver, username)

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "a[href='/']"))
                )
                print(f"{username} のログインが確認されました")
            except Exception as e:
                print(f"{username} のログイン確認に失敗しました: {e}")
                continue

            # ハッシュタグ検索
            logging.info(f"ハッシュタグ '{hashtag}' を検索中...")
            print(f"ハッシュタグ '{hashtag}' を検索中...")
            posts = search_hashtag(driver, hashtag, desired_username)

            # 最近の投稿をフィルタリング
            logging.info(f"最近の投稿をフィルタリング中...")
            filtered_posts = filter_recent_posts(driver, posts, hours=3)

            # 投稿に対する操作
            for post in filtered_posts:
                logging.info(f"投稿に対する操作を実行中: {post}")
                print(f"投稿に対する操作を実行中: {post}")
                interact_with_post(driver, post)

        except Exception as e:
            logging.error(f"エラーが発生しました: {e}")
            print(f"エラーが発生しました: {e}")
        finally:
            driver.quit()
            logging.info(f"{username} の処理が完了しました")
            print(f"{username} の処理が完了しました")


if __name__ == "__main__":
    try:
        # アカウント情報の読み込み
        with open("config/accounts.json", "r") as file:
            accounts = json.load(file)
        
        hashtag = "あざあ"  # 検索するハッシュタグを指定
        desired_username = "djmg.mm"  # 操作対象とするユーザー名を指定（Noneの場合、全投稿が対象）

        logging.info("ツールが実行されました")
        print("ツールが実行されました")
        process_accounts(accounts, hashtag, desired_username=desired_username)

    except Exception as e:
        logging.critical(f"致命的なエラーが発生しました: {e}")
        print(f"致命的なエラーが発生しました: {e}")

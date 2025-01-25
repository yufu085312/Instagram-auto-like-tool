import logging
from utils.login import login_with_cookies
from utils.hashtag_search import search_hashtag, filter_recent_posts
from utils.post_interaction import interact_with_post
from utils.driver_setup import init_driver
import json

# ログ設定
logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def process_accounts(accounts, hashtag, desired_username=None):
    """
    アカウントごとにハッシュタグ検索を実行し、指定された投稿に対して操作を実行します。

    :param accounts: アカウント情報のリスト
    :param hashtag: 検索するハッシュタグ
    :param desired_username: 指定ユーザーの投稿のみを操作する場合に使用
    """
    for account in accounts:
        driver = init_driver()
        try:
            logging.info(f"{account['username']} でログインを試みます")
            print(f"{account['username']} でログインを試みます")
            login_with_cookies(driver, account['username'])

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
            logging.info(f"{account['username']} の処理が完了しました")
            print(f"{account['username']} の処理が完了しました")


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

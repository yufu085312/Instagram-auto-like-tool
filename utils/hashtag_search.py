from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging
import re

# ログ設定
logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def search_hashtag(driver, hashtag):
    """
    Collect posts for a given hashtag using Selenium.
    """
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    print(f"Navigating to hashtag page: {url}")
    driver.get(url)
    time.sleep(5)  # Allow initial page load

    try:
        # Wait for posts to load
        print("Waiting for posts to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/p/"]'))
        )

        print("Posts have loaded. Extracting URLs...")
        posts_script = """
        return Array.from(document.querySelectorAll('a[href^="/p/"]'))
                     .map(a => a.href);
        """
        post_links = driver.execute_script(posts_script)

        # Scroll to load more posts
        print("Scrolling to load more posts...")
        max_scrolls = 10
        for _ in range(max_scrolls):
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)  # Adjust if necessary
            new_post_links = driver.execute_script(posts_script)
            if len(new_post_links) == len(post_links):  # Break if no new posts
                break
            post_links = new_post_links

        print(f"Total posts collected: {len(post_links)}")
        return post_links

    except Exception as e:
        print(f"Error while loading posts: {e}")
        logging.error(f"Error while loading posts: {e}")
        return []


def is_desired_user(driver, desired_username):
    """
    投稿が指定したユーザーのものであるかを確認する（JavaScript オブジェクトから取得）。

    :param driver: Selenium WebDriver
    :param desired_username: 確認するユーザー名
    :return: 指定ユーザーであれば True、それ以外は False
    """
    try:
        # ページソースを取得
        page_source = driver.page_source

        # "user":{"username":"..." の部分を抽出
        match = re.search(r'"user":{"username":"(.*?)"', page_source)
        if match:
            current_username = match.group(1)
            print(f"現在のユーザー名: {current_username}")
            return current_username == desired_username
        else:
            print("ユーザー名がページソースから見つかりませんでした")
            return False

    except Exception as e:
        print(f"ユーザー名の取得中にエラーが発生しました: {e}")
        # デバッグ用にページソースを保存
        with open("debug_user_page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        return False

def filter_recent_posts(driver, posts, hours=3, desired_username=None):
    """
    最近の投稿をフィルタリングし、指定ユーザーの投稿のみを抽出します。

    :param driver: Selenium WebDriver
    :param posts: 投稿URLのリスト
    :param hours: 過去何時間以内の投稿を取得するか
    :param desired_username: 抽出する投稿の指定ユーザー名
    :return: 最近の投稿URLのリスト
    """
    print("最近の投稿をフィルタリングしています...")
    recent_posts = []
    current_time = datetime.utcnow()

    for post_url in posts:
        print(f"投稿URLに移動: {post_url}")
        try:
            # 投稿ページに移動
            driver.get(post_url)

            # ユーザー確認
            if desired_username:
                if not is_desired_user(driver, desired_username):
                    print(f"指定ユーザー '{desired_username}' の投稿ではありません: {post_url}")
                    continue

            # タイムスタンプ要素を待機
            try:
                timestamp_element = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.TAG_NAME, "time"))
                )
                timestamp = timestamp_element.get_attribute("datetime")
                post_time = datetime.fromisoformat(timestamp[:-1])  # UTC形式のタイムスタンプを解析
                print(f"タイムスタンプ: {post_time}")

                # 投稿時間を計算
                if current_time - post_time <= timedelta(hours=hours):
                    recent_posts.append(post_url)
                    print(f"最近の投稿を追加: {post_url}")
                    logging.info(f"最近の投稿を追加: {post_url}")

            except Exception as e:
                print(f"タイムスタンプの取得中にエラーが発生しました: {e}")
                logging.warning(f"タイムスタンプの取得中にエラーが発生しました: {e}")
                continue  # タイムスタンプ取得に失敗した場合はスキップ

        except Exception as e:
            print(f"投稿ページへの移動中にエラーが発生しました: {e}")
            logging.warning(f"投稿ページへの移動中にエラーが発生しました: {e}")
            continue  # ページ移動に失敗した場合はスキップ

    print(f"フィルタリングされた投稿数: {len(recent_posts)}")
    logging.info(f"フィルタリングされた投稿数: {len(recent_posts)}")
    return recent_posts

from datetime import datetime, timedelta
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

# ログ設定
logging.basicConfig(
    filename="logs/execution.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def search_hashtag(driver, hashtag, desired_username=None):
    """
    指定したハッシュタグページを検索し、投稿リンクを収集します（JavaScript を使用）。

    :param driver: Selenium WebDriver
    :param hashtag: ハッシュタグ
    :param desired_username: 指定ユーザー名（Noneの場合、全投稿を収集）
    :return: 投稿リンクのリスト
    """
    url = f"https://www.instagram.com/explore/tags/{hashtag}/"
    print(f"Navigating to hashtag page: {url}")
    driver.get(url)
    time.sleep(6)  # ページロード待機

    post_links = []
    previous_post_count = 0
    try:
        print("Waiting for posts to load...")
        WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[href^="/p/"]'))
        )
        print("Posts have loaded. Extracting URLs...")

        # JavaScript を使って投稿リンクを収集するスクリプト
        posts_script = """
            return Array.from(document.querySelectorAll('a[href^="/p/"]'))
                        .map(a => a.href);
        """

        max_scrolls = 20  # スクロール回数を制限
        for scroll in range(max_scrolls):
            # JavaScript を使って投稿リンクを収集
            new_post_links = driver.execute_script(posts_script)
            for post_url in new_post_links:
                if post_url not in post_links:
                    post_links.append(post_url)
                    print(f"Collected post: {post_url}")

            # スクロールでさらに投稿をロード
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

            # 新しい投稿がロードされていなければ終了
            if len(post_links) == previous_post_count:
                print(f"No new posts loaded after {scroll + 1} scrolls.")
                break
            previous_post_count = len(post_links)

        print(f"Total posts collected: {len(post_links)}")
        return post_links

    except Exception as e:
        print(f"Error while loading posts: {e}")
        logging.error(f"Error while loading posts: {e}")
        return []


def is_desired_user(driver, desired_username):
    """
    投稿が指定したユーザーのものであるかを確認する（ページソースから取得）。

    :param driver: Selenium WebDriver
    :param desired_username: 確認するユーザー名
    :return: 指定ユーザーであれば True、それ以外は False
    """
    try:
        # ページソースを取得
        page_source = driver.page_source

        # "user":{"username":"..." の部分を抽出
        import re
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
        return False


def filter_recent_posts(driver, posts, hours=3):
    """
    最近の投稿を時間ベースでフィルタリングします。

    :param driver: Selenium WebDriver
    :param posts: 投稿URLのリスト
    :param hours: 過去何時間以内の投稿を取得するか
    :return: 最近の投稿URLのリスト
    """
    print("最近の投稿をフィルタリングしています...")
    recent_posts = []
    current_time = datetime.utcnow()

    for post_url in posts:
        print(f"投稿URLに移動: {post_url}")
        try:
            driver.get(post_url)

            # タイムスタンプを取得
            timestamp_element = WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "time"))
            )
            timestamp = timestamp_element.get_attribute("datetime")
            post_time = datetime.fromisoformat(timestamp[:-1])
            print(f"タイムスタンプ: {post_time}")

            # 投稿時間を計算
            if current_time - post_time <= timedelta(hours=hours):
                recent_posts.append(post_url)
                print(f"最近の投稿を追加: {post_url}")
                logging.info(f"最近の投稿を追加: {post_url}")

        except Exception as e:
            print(f"Error retrieving post timestamp: {e}")
            logging.warning(f"Error retrieving post timestamp: {e}")

    print(f"フィルタリングされた投稿数: {len(recent_posts)}")
    logging.info(f"フィルタリングされた投稿数: {len(recent_posts)}")
    return recent_posts

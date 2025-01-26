from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


def interact_with_post(driver, post_url):
    driver.get(post_url)

    try:
        # いいねボタンをクリック
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//span//*[name()='svg' and @aria-label='Like']"))
        )
        like_button = driver.find_element(By.XPATH, "//span//*[name()='svg' and @aria-label='Like']")
        like_button.click()
        print(f"いいね成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"いいね失敗: {e}")

    try:
        # 保存ボタンをクリック
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='Save']"))
        )
        save_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='Save']")
        save_button.click()
        print(f"保存成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"保存失敗: {e}")

    try:
        # シェアボタンをクリック
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "svg[aria-label='share']"))
        )
        share_button = driver.find_element(By.CSS_SELECTOR, "svg[aria-label='share']")
        share_button.click()
        print(f"シェア成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"シェア失敗: {e}")

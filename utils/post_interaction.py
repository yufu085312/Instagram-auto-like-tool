from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def interact_with_post(driver, post_url):
    driver.get(post_url)

    try:
        # Wait for the "Like" button and click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_aamw"))
        )
        like_button = driver.find_element(By.CLASS_NAME, "_aamw")
        like_button.click()
        print(f"いいね成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"いいね失敗: {e}")

    try:
        # Wait for the "Save" button and click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button svg[aria-label="保存"]'))
        )
        save_button = driver.find_element(By.CSS_SELECTOR, 'button svg[aria-label="保存"]')
        save_button.click()
        print(f"保存成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"保存失敗: {e}")

    try:
        # Wait for the "Share" button and click it
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button svg[aria-label="共有"]'))
        )
        share_button = driver.find_element(By.CSS_SELECTOR, 'button svg[aria-label="共有"]')
        share_button.click()
        print(f"シェア成功: {post_url}")
        time.sleep(2)
    except Exception as e:
        print(f"シェア失敗: {e}")

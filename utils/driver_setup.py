from selenium import webdriver
from selenium_stealth import stealth

def init_driver():
    """
    WebDriverを初期化し、Selenium Stealthを設定します。
    """
    try:
        options = webdriver.ChromeOptions()
        options.add_argument("--start-maximized")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36")

        driver = webdriver.Chrome(options=options)

        stealth(driver,
                languages=["en-US", "en"],
                vendor="Google Inc.",
                platform="Win32",
                webgl_vendor="Intel Inc.",
                renderer="Intel Iris OpenGL Engine",
                fix_hairline=True,
        )

        print("WebDriverが正常に初期化されました")
        return driver
    except Exception as e:
        print(f"WebDriverの初期化に失敗しました: {e}")
        raise

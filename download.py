import sys
import time

from selenium import webdriver

def slow_get_selenium(url, interval=2.0):
    time.sleep(interval)

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver = webdriver.Chrome(options=options)
    driver.get(url)

    return driver.page_source


if __name__ == "__main__":
    url = sys.argv[1]
    html = slow_get_selenium(url)
    sys.stdout.write(html)
    sys.stdout.flush()

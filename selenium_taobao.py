# -*- coding:utf-8 -*-

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


browser = webdriver.Chrome(ChromeDriverManager().install())
wait = WebDriverWait(browser, 10)

def search():
    try:
        browser.get("https://www.taobao.com")
        input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))

        submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
        input.send_keys('美食')
        submit.click()
        total = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div >div.total')))
        return total.text
    except TimeoutException:
        return search()

def main():
    total = search()
    print (total)

if __name__ == '__main__':
    main()

from selenium import webdriver
from bs4 import BeautifulSoup
import time


options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/92.0.4515.131 ""Safari/537.36")


driver = webdriver.Chrome(options=options)


def get_soup(keyword):
    url = 'https://www.amazon.ca/'
    driver.get(url)
    driver.maximize_window()

    search_box = driver.find_element_by_id("twotabsearchtextbox")
    search_box.send_keys(keyword)
    search_box.submit()

    sort = driver.find_element_by_id('a-autoid-0-announce')
    sort.click()

    av_reviews = driver.find_element_by_id('s-result-sort-select_3')
    av_reviews.click()

    time.sleep(1)
    driver.save_screenshot('local_ss.png')

    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    return soup


print(get_soup('rope'))

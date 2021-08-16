from selenium import webdriver
from bs4 import BeautifulSoup
import time
import pandas as pd
import matplotlib.pyplot as plt


options = webdriver.ChromeOptions()
options.add_argument("--headless")
# options.add_argument("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
#                     "Chrome/92.0.4515.131 ""Safari/537.36")


driver = webdriver.Chrome(options=options)

keyword = input("What would you like to search Amazon.ca for? ")


def get_soup(search_term):
    url = 'https://www.amazon.ca/'
    driver.get(url)
    driver.maximize_window()

    search_box = driver.find_element_by_id("twotabsearchtextbox")
    search_box.send_keys(search_term)
    search_box.submit()

    '''sort = driver.find_element_by_id('a-autoid-0-announce')
    sort.click()

    av_reviews = driver.find_element_by_id('s-result-sort-select_3')
    av_reviews.click()'''

    time.sleep(1)
    # driver.save_screenshot('local_ss.png')

    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')

    return soup


def get_data():
    names_list = []
    prices_list = []

    soup = get_soup(keyword)

    names = soup.find_all("span", {'class': 'a-size-base-plus a-color-base a-text-normal'})
    for name in names:
        names_list.append(name.text)

    prices = soup.find_all("span", {'class': 'a-price-whole'})
    for price in prices:
        price_clean = price.text[:-1].replace(',', '')
        prices_list.append(int(price_clean))

    return names_list[:len(prices_list)], prices_list


def create_dataframe():
    names, prices = get_data()

    dictionary = {'Name': names, 'Price ($)': prices}

    df = pd.DataFrame(dictionary)
    df['Search Term'] = keyword

    return df


def create_bp():
    bp = df.boxplot(by=['Search Term'], column=['Price ($)'], grid=False, showmeans=True)
    bp.set_title("Boxplot of '" + str(keyword) + "' Price")
    bp.set_xlabel("")
    bp.set_ylabel("Price ($)")

    plt.suptitle('')
    plt.savefig('boxplot.png')


def save_to_excel():
    writer = pd.ExcelWriter('Amazon Web-Scraper.xlsx')
    df.to_excel(writer, sheet_name='Data', index=False)

    bpsheet = writer.sheets['Data']
    bpsheet.insert_image('E2', 'boxplot.png')

    writer.save()
    print('saved files')


if __name__ == '__main__':
    df = create_dataframe()
    create_bp()
    save_to_excel()

from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# CHROME WEBDRIVER
chrome_driver_path = 'C:\Program Files\Google\Chrome\Application\chromedriver'
browser = webdriver.Chrome(chrome_driver_path)
productLinks = []
base_url = "https://www.idefix.com"


def scrape_book_links(url):  # Finds links of the books and returns
    r = requests.get(url).content
    soup = BeautifulSoup(r, "html.parser")
    product_list = soup.find_all('div', {
        'class': "col-12 col-xl-3 col-lg-4 col-md-6 col-sm-6 col-xs-6-product catalog-list-carousel itemlittleProduct"})

    for item in product_list:
        for link in item.find_all('a', {'class': "product-image"}, href=True):
            productLinks.append(base_url + link['href'])


browser.get('https://www.idefix.com/kategori/Kitap/Bilim/grupno=00052')
# closes cookie popup
time.sleep(5)
closeCookie = browser.find_element_by_xpath('//*[@id="cookieConsentContainer"]/div[1]/div/a')
closeCookie.click()

# goes through all pages in Science category of Idefix, for each page calls Book Link Scraper function to gather book links.
pageClass = browser.find_element_by_xpath('//*[@id="catPageContent"]/div[2]/div[1]/div[5]/div/div[3]/div[3]')
pageSelector = pageClass.find_element_by_tag_name('ul')
pages = pageSelector.find_elements_by_tag_name('li')
for i in range(66):  # number of pages in specific category
    url = browser.current_url
    scrape_book_links(url)
    pages = pageSelector.find_elements_by_tag_name('li')
    pages[-1].click()
    time.sleep(2)
#print(productLinks)

browser = webdriver.Chrome(chrome_driver_path)
science_books_list = []

# Gets all book urls from the former cell and scrapes needed data into dict
# This takes 1 hour or so because of time.sleep(1), to get books without getting blocked

for book_url in productLinks:
    browser.get(book_url)
    try:
        book_name = browser.find_element_by_xpath("//span[text()='Kitap Adı:']/ancestor::li").text.split(": ")[1]
    except:
        book_name = np.NaN
    try:
        author_name = browser.find_element_by_xpath(
            '//*[@id="selectedId"]/section[2]/div[2]/div/div/div/div/div/div[1]/div/ul/li[2]/span[2]/a').text.strip()
    except:
        author_name = np.NaN
    try:
        book_rate = browser.find_element_by_xpath(
            '//*[@id="productpricedetails"]/div[1]/div[2]/span/span[1]').text.strip() + "/5"
    except:
        book_rate = np.NaN
    try:
        number_of_raters = browser.find_element_by_xpath(
            '//*[@id="productpricedetails"]/div[1]/div[2]/span/span[3]').text.strip()
    except:
        number_of_raters = np.NaN
    try:
        book_sale_price = browser.find_element_by_xpath('//*[@id="salePrice"]').text.strip()
    except:
        book_sale_price = np.NaN

    try:
        number_of_pages = browser.find_element_by_xpath("//span[text()='Sayfa Sayısı:']/ancestor::li").text.split(": ")[
            1]
    except:
        number_of_pages = np.NaN

    try:
        publication_year = \
        browser.find_element_by_xpath("//span[text()='İlk Baskı Yılı:']/ancestor::li").text.split(": ")[1]

    except:
        publication_year = np.NaN

    book_data = {
        'Name': book_name,
        'Author': author_name,
        'Price': book_sale_price,
        'Number of Pages': number_of_pages,
        'Publication Year': publication_year,
        'Book Rate': book_rate,
        'Number of Raters': number_of_raters,
    }

    science_books_list.append(book_data)
    time.sleep(1)

book_df = pd.DataFrame(science_books_list)
book_df.to_csv('book_df', index = False)
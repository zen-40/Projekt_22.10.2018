from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests
import re


class Settings:
    """My class with settings website and cookies elements"""
    def __init__(self, url):
        self.url = url
        requests.get(url, headers={'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}, timeout=15)
        html = urlopen(url)
        self.soup = BeautifulSoup(html, 'lxml')
        type(self.soup)


    def soup_element(self):
        return self.soup


# Function use in Action 2
def dry_form(my_element):
    cleaner = re.sub(' ', '', my_element.lower())
    return cleaner


# Basic variables
WEBSITE = 'https://www.auchandirect.pl/auchan-warszawa/pl/search?' \
          'text=pepsi+cola&callback=true'
settings_website = Settings(WEBSITE)
soup_obj = settings_website.soup_element()
auchan_website = 'https://www.auchandirect.pl%s'
products_links = soup_obj.findAll('a', class_='display')
links = []
scrape_data = []


#Acction_1 - Scrape all product links and add to list 'links'
for link in products_links:
    links.append(auchan_website%link.get('href'))


#Action_2 - Scrape all data (like title, price, image, packaging) and add to list 'scrape_data'
for products in links:
    # 'for products' settings website
    WEBSITE = products
    settings_website = Settings(WEBSITE)
    soup_obj_1 = settings_website.soup_element()

    # Scrap title
    scrape_data.append(soup_obj_1.title.text)

    # Scrap price
    products_links_price = soup_obj_1.find(class_='packaging')
    extract_str = products_links_price.strong.extract()
    scrape_data.append(products_links_price.text.strip())

    # Scrap link image
    products_links_image = soup_obj_1.findAll(class_="carousel-item")
    scrape_data.append(auchan_website%products_links_image[0].img['data-src'])
    
    # Scrap packaging.
    envir_list_basic = []
    envir_list_check = []
    products_links_packing = soup_obj_1.findAll('p')
    for products in products_links_packing:
        envir_list_basic.append(products.text)
        envir_list_check.append(dry_form(products.text))
    comp_element = dry_form(extract_str.text)
    if comp_element in envir_list_check:
        scrape_data.append(envir_list_basic[envir_list_check.index(comp_element) - 1])


# RESULT IN LIST 'SCRAPE_DATA'
print(scrape_data)
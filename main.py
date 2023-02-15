import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests
import time

Z_URL = "https://www.zillow.com/homes/for_rent/1-_beds/?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3Anull%2C%22mapBounds%22%3A%7B%22west%22%3A-122.56276167822266%2C%22east%22%3A-122.30389632177734%2C%22south%22%3A37.69261345230467%2C%22north%22%3A37.857877098316834%7D%2C%22isMapVisible%22%3Atrue%2C%22filterState%22%3A%7B%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22mp%22%3A%7B%22max%22%3A3000%7D%2C%22price%22%3A%7B%22max%22%3A872627%7D%2C%22beds%22%3A%7B%22min%22%3A1%7D%7D%2C%22isListVisible%22%3Atrue%2C%22mapZoom%22%3A12%7D"
Z_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.5481.77 Safari/537.36",
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8"
}

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSfo_Dp3VB_nrCWn6O6DMnYpkhKGQlY5YWlC2cPpKzAeL0Xu-A/viewform?usp=sf_link"

CHROME_DRIVER_PATH = "C:\python\chromedriver.exe"
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)

def zillow_scraper():
    response = requests.get(Z_URL, headers=Z_HEADERS)
    zillow_webpage = response.text

    soup = BeautifulSoup(zillow_webpage, "html.parser")

    addresses = soup.find_all('address')
    links = soup.find_all(class_='StyledPropertyCardDataArea-c11n-8-84-2__sc-yipmu-0 cTLZKy property-card-link')
    prices = soup.find_all(class_="StyledPropertyCardDataArea-c11n-8-84-2__sc-yipmu-0 gugdBn")
    # print(len(prices))
    # print(len(addresses))
    # print(len(links))
    output_addresses = [addresses[i].text for i in range(len(addresses))]
    output_links = []
    output_prices = [prices[i].text for i in range(len(addresses))]
    # print(output_addresses)
    # print(output_prices)
    for l in range(len(links)):
        link = links[l].get('href')
        if 'zillow' not in link:
            link = 'https://zillow.com' + link
        output_links.append(link)

    return output_addresses, output_links, output_prices
    # Line 30 needs to have 'https://www.zillow.com' in front href's if its not already present


def form_fill_out(dictionary):
    for i in range(len(dictionary['addresses'])):
    # implement selenium to enter info into your google form
        driver = webdriver.Chrome(service=Service(CHROME_DRIVER_PATH), options=chrome_options)
        driver.get(FORM_URL)
        driver.maximize_window()
        time.sleep(1)
        address = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[1]/div/div/div[2]/div/div[1]/div/div[1]/input')
        price = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[2]/div/div/div[2]/div/div[1]/div/div[1]/input')
        link = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[2]/div[3]/div/div/div[2]/div/div[1]/div/div[1]/input')
        address.send_keys(dictionary["addresses"][i])
        price.send_keys(dictionary["prices"][i])
        link.send_keys(dictionary["links"][i])
        submit_button = driver.find_element(By.XPATH, '//*[@id="mG61Hd"]/div[2]/div/div[3]/div[1]/div[1]/div')
        submit_button.click()



addresses, links, prices = zillow_scraper()
listings = {
    "addresses": addresses,
    "links": links,
    "prices": prices,
}
form_fill_out(listings)

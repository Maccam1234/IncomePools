import bs4
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
import time

url = 'https://schooladvice.net/2018/01/british-columbia-independent-private-schools/'

browser = webdriver.Chrome()
browser.get(url)
time.sleep(3)

res = browser.find_element(By.XPATH, "//div[(@id='wpupg-grid-schoolfinder-bc') and (@class = 'wpupg-grid wpupg-responsive-desktop')]")
html = res.get_attribute('innerHTML')
soup = bs4.BeautifulSoup(html, 'lxml')

names = []

divs = soup.findAll('h3', class_='wpupg-item-title wpupg-block-text-bold wpupg-align-center')
for name in divs:
    names.append(name.get_text())

print(names)

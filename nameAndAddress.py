import bs4
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

url = 'https://schooladvice.net/2018/01/british-columbia-independent-private-schools/'

#chrome_options = Options()
#chrome_options.add_argument("--headless")
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
browser.quit()

print('----------------------------\nAll school names have been retrieved')

addresses = []
cities = []
postalCodes = []
googleMaps = 'https://www.google.com/maps'

browser = webdriver.Chrome()
for school in names:
    browser.get(googleMaps)
    time.sleep(1)
    searchBox = browser.find_element(By.XPATH, "//input[(@id='searchboxinput') and (@class = 'searchboxinput xiQnY')]")
    searchBox.send_keys(school)
    searchBox.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        address = browser.find_element(By.XPATH, "//div[(@class = 'Io6YTe fontBodyMedium kR99db ')]")
        addressString = address.get_attribute('innerHTML')
        street = addressString[0:addressString.find(',')]
        addressString = addressString[addressString.find(',') + 2:len(addressString)]
        city = addressString[0:addressString.find(',')]
        addressString = addressString[addressString.find(',') + 2:len(addressString)]
        postalCode = addressString[len(addressString) - 7:len(addressString)]
    except:
        street = ''
        city = ''
        postalCode = ''
    addresses.append(street)
    cities.append(city)
    postalCodes.append(postalCode)

data = {
    'School Name': names,
    'Address': addresses,
    'City': cities,
    'Province': 'British Columbia',
    'Country': 'Canada',
    'Postal Codes': postalCodes
}

df = pd.DataFrame(data)
df.to_csv('VancouverPrivateSchools2.csv')
print('monkey')

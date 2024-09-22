import bs4
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

dfnames = pd.read_csv('Library Names - Sheet1.csv')
names = dfnames['Full Name']
addresses = []
cities = []
postalCodes = []
lats = []
longs = []
googleMaps = 'https://www.google.com/maps'

browser = webdriver.Chrome()
for name in names:
    browser.get(googleMaps)
    time.sleep(1)
    searchBox = browser.find_element(By.XPATH, "//input[(@id='searchboxinput') and (@class = 'searchboxinput xiQnY')]")
    searchBox.send_keys(name)
    searchBox.send_keys(Keys.RETURN)
    time.sleep(2)
    try:
        address = browser.find_element(By.XPATH, "//div[(@class = 'Io6YTe fontBodyMedium kR99db ')]")
        addressString = address.get_attribute('innerHTML')
        street = addressString[0:addressString.find(',')]
        addressString = addressString[addressString.find(',')+2:len(addressString)]
        city = addressString[0:addressString.find(',')]
        addressString = addressString[addressString.find(',') + 2:len(addressString)]
        postalCode = addressString[len(addressString)-7:len(addressString)]

        newUrl = browser.current_url
        newUrl = newUrl[newUrl.find('@') + 1:len(newUrl)]
        lat = newUrl[0:newUrl.find(',')]
        newUrl = newUrl[newUrl.find(',') + 1:len(newUrl)]
        long = newUrl[0:newUrl.find(',')]
    except:
        street = ''
        city = ''
        postalCode = ''
        lat = ''
        long = ''
    addresses.append(street)
    cities.append(city)
    postalCodes.append(postalCode)
    lats.append(lat)
    longs.append(long)

data = {
    'School Name': names,
    'Address': addresses,
    'City': cities,
    'Province': 'British Columbia',
    'Country': 'Canada',
    'Postal Codes': postalCodes,
    'Latitude': lats,
    'Longitude': longs
}

df = pd.DataFrame(data)
df.to_csv('LibraryCoordinates.csv')
print('monkey')


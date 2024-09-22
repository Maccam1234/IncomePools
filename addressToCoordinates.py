import bs4
import lxml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import pandas as pd

url = 'https://www.latlong.net/convert-address-to-lat-long.html'

df = pd.read_csv('VancouverPrivateSchoolsOld.csv')
df = df.drop('Unnamed: 0', axis=1)
addresses = df['Address']
lats = []
longs = []

browser = webdriver.Chrome()
for address in addresses:
    browser.get(url)
    time.sleep(1)
    searchBox = browser.find_element(By.XPATH, "//input[(@class = 'width70')]")
    searchBox.send_keys(address)
    searchBox.send_keys(Keys.RETURN)
    time.sleep(2)
    latlong = browser.find_element(By.XPATH, "//span[(@id='latlngspan') and (@class = 'coordinatetxt')]")
    latlongString = latlong.get_attribute('innerHTML')
    lat = latlongString[1:9]
    long = latlongString[11:19]
    lats.append(lat)
    longs.append(long)

df['Latitude'] = lats
df['Longitude'] = longs
df.to_csv('coordinates.csv')
print('monkey')
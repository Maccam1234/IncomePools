import random
import requests
import bs4
import lxml
import pandas as pd
import numpy as np
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import matplotlib.pyplot as plt
from google.colab import drive
from google.colab import output

# browser for loading youtube and wayback
drive.mount('/content/drive/')
# things to make the selenium chrome browser work in colab
service = Service(executable_path=r'chromedriver')
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
browser = webdriver.Chrome(service=service,options=chrome_options)

yturls = pd.DataFrame([
    # ['https://www.youtube.com/results?search_query=education+channels&sp=EgIQAg%253D%253D', 'education'],
    # ['https://www.youtube.com/results?search_query=lifestyle+channels&sp=EgIQAg%253D%253D', 'lifestyle'],
    # ['https://www.youtube.com/results?search_query=cooking+channels&sp=EgIQAg%253D%253D', 'cooking'],
    #  ['https://www.youtube.com/results?search_query=gaming+channels&sp=EgIQAg%253D%253D', 'gaming'],
    ['https://www.youtube.com/results?search_query=fitness+channels&sp=EgIQAg%253D%253D', 'fitness'],
    # ['https://www.youtube.com/results?search_query=vlog+channels&sp=EgIQAg%253D%253D', 'vlog'],
    # ['https://www.youtube.com/results?search_query=reviews+channels&sp=EgIQAg%253D%253D', 'reviews'],
    # ['https://www.youtube.com/results?search_query=beauty+channels&sp=EgIQAg%253D%253D', 'beauty'],
    # ['https://www.youtube.com/results?search_query=asmr+channels&sp=EgIQAg%253D%253D', 'asmr']
], columns=['link', 'name'])



for i in range(0, len(yturls.index)):
    # URLs must have atleast one save on wayback in 2018 or else a blank string will be returned
    # urls will contain urls with the format https://socialblade.com/youtube/user/
    urls = []

    yturl = yturls.at[i, 'link']

    tags = []

    browser.get(yturl)
    print("---------------------------\nstarting youtube search and scrape")
    tic = time.perf_counter()
    # scrolls until youtube has no more results
    while True:
        # end_result = "No more results" string at the bottom of the page
        # this will be used to break out of the while loop
        try:
            end_result = browser.find_element(By.XPATH, "//yt-formatted-string[(@id='message') and "
                                                        "(@class = 'style-scope ytd-message-renderer')]").is_displayed()
        except:
            end_result = False
        browser.execute_script("var scrollingElement = (document.scrollingElement || document.body);"
                               "scrollingElement.scrollTop = scrollingElement.scrollHeight;")

        # once element is located, break out of the loop
        if end_result == True:
            break

    res = browser.find_element(By.XPATH,
                               "//div[(@id='contents') and (@class = 'style-scope ytd-section-list-renderer')]")
    html = res.get_attribute('innerHTML')
    soup = bs4.BeautifulSoup(html, 'lxml')
    # gets all the yt tags
    divs = soup.findAll('span', id='subscribers', class_='style-scope ytd-channel-renderer')

    # adds each tag to the tags array
    for tag in divs:
        tags.append(tag.get_text())

    # results 1-300 or 300+
    tags = tags[0:300]
    # tags = tags[300:len(tags)]

    # adds each tag to the base url to get the channels' social blade url and adds it to urls array
    for tag in tags:
        urls.append('https://socialblade.com/youtube/user/' + tag[1:len(tag)])

    toc = time.perf_counter()
    print(f"Finished scrapping social blade links from youtube in {(toc - tic) / 60:0.4f} minutes")

    df2023 = pd.DataFrame(columns=['Channel Name', 'Country', 'Channel Type', 'User Creation Date', 'Uploads 2023',
                                   'Subscribers 2023', 'Video Views 2023'])

    # used to get around socialblade bot detection by pretending to be a user
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
        "Referer": "https://targetwebsite.com/page1"
    }

    # scrape 2023 data from social blade
    print('-----------------------------\nstarting social blade scrape')
    tic = time.perf_counter()
    for x in range(0, len(urls)):
        url = urls[x]
        try:
            # random time intervals to bypass bot detection
            time.sleep(random.random() * 3 + random.random())
            res = requests.get(url, headers=headers)
            soup = bs4.BeautifulSoup(res.content, 'lxml')

            divs = soup.find('div', id='YouTubeUserTopInfoBlockTop')
            # get first div within YouTubeUserTopInfoBlockTop which is where the channel name is
            titleDiv = divs.find('div')
            title = titleDiv.find('h1')
            channelName = title.get_text().strip()
            # will become an array containing all the info for the channel
            channelInfo = [channelName]

            divs = divs.find('div', id='YouTubeUserTopInfoBlock')
            divs = divs.findAll('div', class_='YouTubeUserTopInfo')
            # just to get creation date, country, channel type before the numbers
            for x in range(3, len(divs)):
                div = divs[x]
                header = div.find('span', class_='YouTubeUserTopLight')
                content = div.find('span', attrs={'style': 'font-weight: bold;'}).get_text()
                while content.find(',') != -1:
                    content = content[0:content.find(',')] + content[content.find(',') + 1:len(content)]
                channelInfo.append(content)
            # get the uploads, views and subs after
            for x in range(0, 3):
                div = divs[x]
                header = div.find('span', class_='YouTubeUserTopLight')
                content = div.find('span', attrs={'style': 'font-weight: bold;'}).get_text()
                while content.find(',') != -1:
                    content = content[0:content.find(',')] + content[content.find(',') + 1:len(content)]
                channelInfo.append(content)

            # Insert new row of channelInfo
            df2023.loc[len(df2023.index)] = channelInfo
        except:
            df2023.loc[len(df2023.index)] = ['', '', '', '', '', '', '']

    toc = time.perf_counter()
    print(f"Finished social blade scrape in {(toc - tic) / 60:0.4f} minutes")

    waybackUrls = []

    # gets the wayback urls using the socialblade urls
    print('-----------------------------\nstarting to get wayback urls from social blade urls')
    tic = time.perf_counter()
    for url in urls:
        # bring us to the 2018 calendar for the socialblade site
        url = 'https://web.archive.org/web/20180101000000*/' + url
        # opens the link in chrome, run twice incase the first time doesn't work
        browser.get(url)
        browser.get(url)

        try:
            # browser probably takes 3 seconds to load
            time.sleep(5)
            # find the html within calendar-grid div
            res = browser.find_element(By.CLASS_NAME, 'calendar-grid')
            html = res.get_attribute("innerHTML")
            soup = bs4.BeautifulSoup(html, 'lxml')

            # finding the first href in the calendar (which will be the first save in 2018)
            link = soup.find('a')
            link = 'https://web.archive.org' + link['href']
            waybackUrls.append(link)
        except:
            # if no saves in 2018
            waybackUrls.append('')

    toc = time.perf_counter()
    print(f"Finished scrapping for wayback urls in {(toc - tic) / 60:0.4f} minutes")

    df2018 = pd.DataFrame(columns=['Uploads 2018', 'Subscribers 2018', 'Video Views 2018'])

    # scrapes for 2018 data on wayback
    print('-----------------------------------\nstarting to scrape wayback')
    tic = time.perf_counter()
    for url in waybackUrls:
        try:
            res = requests.get(url)
            channelInfo = []
            soup = bs4.BeautifulSoup(res.content, 'lxml')

            divs = soup.find('div', id='YouTubeUserTopInfoBlockTop')

            divs = divs.find('div', id='YouTubeUserTopInfoBlock')
            # all divs in the top bar (subs, views, country, creation date, ...)
            divs = divs.findAll('div', class_='YouTubeUserTopInfo')
            # only need subs views and uploads from 2018 because everything else is already saved from 2023
            for x in range(0, 3):
                div = divs[x]
                header = div.find('span', class_='YouTubeUserTopLight')
                content = div.find('span', attrs={'style': 'font-weight: bold;'}).get_text()
                # gets rid of commas in the numbers
                while content.find(',') != -1:
                    content = content[0:content.find(',')] + content[content.find(',') + 1:len(content)]
                channelInfo.append(content)

            # Insert new row of channelInfo
            df2018.loc[len(df2018.index)] = channelInfo
        except:
            df2018.loc[len(df2018.index)] = ['', '', '']

    toc = time.perf_counter()
    print(f"Finished scrapping wayback in {(toc - tic) / 60:0.4f} minutes")

    dfFinal = pd.concat([df2023, df2018], axis=1)
    dfFinal['Video Views 2023'] = pd.to_numeric(dfFinal['Video Views 2023'])
    dfFinal['Video Views 2018'] = pd.to_numeric(dfFinal['Video Views 2018'])
    dfFinal['Subscribers 2018'] = pd.to_numeric(dfFinal['Subscribers 2018'])

    # this is to convert the 2023 subscriber count from nM to a number in the form n000000 then make it a float
    for x in range(0, len(dfFinal['Subscribers 2023'])):
        multiplier = 1
        if dfFinal.at[x, 'Subscribers 2023'].find('M') != -1:
            dfFinal.at[x, 'Subscribers 2023'] = dfFinal.at[x, 'Subscribers 2023'][0:len(dfFinal.at[x,
            'Subscribers 2023']) - 1]
            multiplier = 1000000
        if dfFinal.at[x, 'Subscribers 2023'].find('K') != -1:
            dfFinal.at[x, 'Subscribers 2023'] = dfFinal.at[x, 'Subscribers 2023'][0:len(dfFinal.at[x,
            'Subscribers 2023']) - 1]
            multiplier = 1000
        dfFinal.at[x, 'Subscribers 2023'] = pd.to_numeric(dfFinal.at[x, 'Subscribers 2023']) * multiplier

    dfFinal.to_csv("drive/My Drive/Cameron Summer Research/Data/newyoutuberData_{}_2018_2023_1_300.csv".format(yturls.at[i, 'name']))

    print('-----------------------------------\n\nDone this iteration!\n')

# Beep sound to signify code is completed
output.eval_js('new Audio("https://upload.wikimedia.org/wikipedia/commons/0/05/Beep-09.ogg").play()')

#! /usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import csv
from datetime import date, datetime
from pandas import *

baseUrl = "https://www.idfa.nl"
links = []
titles = []
items = []
directors = []
countries = []
years = []
metaList = []

pageCounter = 1

# 1. Fetch the data from the website
while True:
    URL = ("https://www.idfa.nl/en/collection/documentaries?page=" + str(pageCounter) + "&filters[tvPrice]=Free")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    linksRaw = soup.find_all("a", class_="collectionitem-module__link___2NQ6Q")
    titlesRaw = soup.find_all("h2", class_="collectionitem-module__title___1Cpb- type-module__title___2UQhK")
    metaBlock = soup.find_all("ul", class_="metainfo-module__meta___1T338 type-module__default___3yLbV collectionitem-module__meta___2_KWS type-module__defaultSmall___3bbtW")
    if linksRaw == []: # end of search pages reached
        break
    # FOR TESTING PURPOSES
    # if pageCounter == 2:
    #     break
    # 2. Select from data: director, title, country, year, duration
    # 3. Put all this in a bunch of variables
    for link in linksRaw:
        url = link.get('href')
        links.append(baseUrl + url)
    for ttl in titlesRaw:
        title = ttl.text
        titles.append(title)
    for ul in metaBlock:
        itemList = []
        for item in ul:
            itemText = item.text
            itemList.append(itemText)
        metaList.append(itemList)            
    pageCounter += 1
    continue

# 3. Open csv file with the local film list 
colnames = ["title", "director", "country", "year", "duration", "url", "timestamp"]
data = read_csv("library.csv", names=colnames)
existing_urls = data.url.tolist()

# 4. Check for each film in the variables if it's already in the local film list. Assume url is unique. 
counter = 0
f = open('library.csv','a')
for url in links:
    # 6. If no, add to the list with timestamp
    if url not in existing_urls:
        if len(metaList[counter]) >= 4:
            if "min" in metaList[counter][3]:
                writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)
                writer.writerow((titles[counter], metaList[counter][0], metaList[counter][1], metaList[counter][2], metaList[counter][3], links[counter], date.today())) 
    # 5. If yes, skip
    counter += 1
f.close()

# 7. Convert the local film list into an alphabetised HTML page
open('index.html', 'w').close()
with open("head.html") as file:
    header = file.read()
    file.close()
file = open("index.html", "a")
file.write(header)

with open('library.csv', 'r') as library:
    library_list = csv.reader(library)
    library_list = sorted(library_list, key=lambda row: row[6], reverse=True)
    newest = datetime.strptime(library_list[0][6], '%Y-%m-%d')
    print(newest)
    last_added = date.today()-newest.date()
    print(last_added)
    if last_added.days<1:
        new_added = ("New films added today. ")
    elif last_added.days<2:
        new_added = ("New films added yesterday. ")
    elif last_added.days<7:
        new_added = ("New films added ", ("%d days" % last_added.days), " ago. ")
    else: 
        new_added = ''

dateStamp = "<p>", ''.join(new_added), "Last refreshed on: ", date.today().strftime("%d/%m/%Y"), "</p>"
dateStamp = ''.join(dateStamp)
file.write(dateStamp)

file.write("<ol type='1'>")
with open('library.csv', 'r') as library:
    library_list = csv.reader(library)
    library_list = sorted(library_list, key=lambda row: row[0])
    libcsv = list(library_list)
    for line in libcsv:
        line_to_write = ("<li><i><b>" + line[0] + "</b></i>, " + line[1] + ", " + line[2] + " (" + line[3] + "), " + line[4] + ". <a href='" + line[5] + "'' target='_blank'>" + "<span class='glyphicon glyphicon-new-window'></span>" + "</a>")
        time_stamp = datetime.strptime(line[6], '%Y-%m-%d')
        added = date.today()-time_stamp.date()
        # 8. If timestamp of the film is > (TODAY -7 days), then print it with a 'new' label
        if added.days<7:
            file.write(line_to_write + " <b class='new'> NEW</b> " +"</li>")
        # 9. Else, just print it
        else:
            file.write(line_to_write + "</li>")
file.write("</ol></body></html>")
file.close()





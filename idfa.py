#! /usr/local/bin/python3

import requests
from bs4 import BeautifulSoup
import csv

baseUrl = "https://www.idfa.nl"
links = []
titles = []
items = []
directors = []
countries = []
years = []
metaList = []

pageCounter = 1

while True:
    URL = ("https://www.idfa.nl/en/collection/documentaries?page=" + str(pageCounter) + "&filters[tvPrice]=Free")
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    linksRaw = soup.find_all("a", class_="collectionitem-module__link___2NQ6Q")
    titlesRaw = soup.find_all("h2", class_="collectionitem-module__title___1Cpb- type-module__title___2UQhK")
    metaBlock = soup.find_all("ul", class_="metainfo-module__meta___1T338 type-module__default___3yLbV collectionitem-module__meta___2_KWS type-module__defaultSmall___3bbtW")
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
    if pageCounter == 49:
        break
    else:
        continue

totalNumber = len(links)
data_to_save = []
counter = 0

open('index.html', 'w').close()
with open("head.html") as f:
    s = f.read()
f = open("index.html", "a")
f.write(s)
f.write("<ol type='1'>")
while True:
    if len(metaList[counter]) >= 4:
        if "min" in metaList[counter][3]:
            f = open("index.html", "a")
            f.write("<li><i><b>" + titles[counter] + "</b></i>, " + metaList[counter][0] + ", " + metaList[counter][1] + " (" + metaList[counter][2] + "), " + metaList[counter][3] + ". <a href='" + links[counter] + "'>" + "Visit on idfa.nl" + "</a>"+ "</li>")
    counter += 1
    if counter == totalNumber:
        break
f.write("</ol>")
f.close()

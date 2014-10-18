#!/usr/bin/python3
#!python3

import codecs
# using requests (2.4.0)
import requests
# using beautifulsoup4 (4.3.2)
from bs4 import BeautifulSoup, SoupStrainer

def airportCodeSearch(strLetter):
    payload = {'iataaptlst':strLetter, 'icaoaptlst':'', 'B1':'Submit'}
    req = requests.post("http://www.avcodes.co.uk/aptlistres.asp", data=payload, headers={'Connection':'close'})
    txtR = req.text.encode('utf-8')
    req.connection.close()
    # make a soup
    soup = BeautifulSoup(txtR, "html.parser")
    # find table which is having class value "ink-table alternating"
    tagTR = soup.find_all("table", "ink-table alternating")
    # go through resultset & get all TD tags value
    searchData = ''
    for value in tagTR[0]:
        valueType = str(value.encode('utf-8'))
        reSoup = BeautifulSoup(valueType, "html.parser")
        tagTD = reSoup.find_all("td")
        actualValue = ''
        # 6 columns availble from the site.. creating json obj
        if (len(tagTD) == 6):
            iataCode = (tagTD[0].text).encode().decode('utf-8')
            icaoCode = (tagTD[1].text).encode().decode('utf-8')
            locationName = (tagTD[2].text).encode().decode('utf-8')
            airPortName = (tagTD[3].text).encode().decode('utf-8')
            countryName = (tagTD[4].text).encode().decode('utf-8')
            cityName = (tagTD[5].text).encode().decode('utf-8')
            jsonValue = '{"iataCode":"' + iataCode + '","icaoCode":"' + icaoCode + '","locationName":"' + locationName
            jsonValue += '","airPortName":"' + airPortName + '","countryName":"' + countryName + '","cityName":"' + cityName + '"},'
            searchData += jsonValue.replace('\\','\\\\')
        # actual values
        searchData += actualValue if(actualValue != "") else ""
    # return the concated result
    return searchData

# main variable to hods value for airport codes
jsonData = ''
a2z = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
# fetch data for each alphabets
for x in range(len(a2z)):
    jsonData += airportCodeSearch(a2z[x])

# should have some data
if(jsonData != ""):
    # remove last 'comma (,)' from the string
    jsonData = jsonData[:-1]
    # create json file
    file = codecs.open("airport-code.json", "wb", "utf-8")
    file.write("[\n" + jsonData + "\n]")
    file.close()
    print('JSON created!')
else:
    print('No Data Found!')
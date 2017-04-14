import requests
from bs4 import BeautifulSoup
from selenium import  webdriver
from selenium.webdriver.common.keys import Keys
from textblob import TextBlob
import pyzillow
import re
import csv
import pandas
import matplotlib.pyplot as plt
from collections import OrderedDict
from HousingScrape import *


object = ZillowScrape()
#object.__init__()
#print(object.base_url)
#object.buy_or_rent()
#print(object.initialScrape())




zillowAddress = 'https://www.zillow.com/homes/for_rent/Providence-RI-02903/house,condo,apartment_duplex,mobile,townhouse_type/58978_rid/41.853196,-71.359635,41.763245,-71.493702_rect/12_zm/'
response = requests.get(zillowAddress)
PureHTML = response.content
HTMLPretty = BeautifulSoup(PureHTML)

#print (HTMLPretty.prettify())

spans = []
for li in HTMLPretty.find_all('span'):
    spans.append(li)

#print(spans)




AddressSpans = HTMLPretty.find_all('span', {'itemprop' : 'streetAddress'})
PriceSpans = HTMLPretty.find_all('span', {'class' : 'zsg-photo-card-price'})
BedSpans = HTMLPretty.find_all('span', {'class' : 'zsg-photo-card-info'})
GeoSpans = HTMLPretty.find_all('span', {'itemprop' : 'geo'})



print(AddressSpans)
print(PriceSpans)
print(BedSpans)
print(GeoSpans)

strAddress = []
strPrice = []

for item in AddressSpans:  # Correct
    print(item.string)
    strAddress.append(item.string)

for item in PriceSpans:    #Correct
    print(item.string)
    var = item.string
    var = var.strip('o')
    var = var.strip('m')
    var = var.strip('/')
    var = var.strip('$')
    int_b = int(var.replace(',',''))
    strPrice.append(int_b)


for item in HTMLPretty.find_all('span', {'class' : 'zsg-photo-card-info'}):
    links = item.findAll('span')
    #print(links)
    #print(item)  #whole item with the room detaisl

#for item in BedSpans:      #Houses w/multiple rooms to rent
#    print(item)

for item in GeoSpans: #not really necessary if we havean address
    print(item)


strAddress.insert(0,'Addresses')
strPrice.insert(0, 'Rent')

print('*****************')
print(strAddress)
print(strPrice)
print('*****************')
Houses_Dict = {}
Houses_Dict = OrderedDict(zip(strAddress, strPrice))


#Doesnt keep the items sorted
#for i in range(len(strAddress)):
    #Houses_Dict[strAddress[i]] = strPrice[i]

print(Houses_Dict)


with open('RIHousing.csv', 'w') as out:
    writer = csv.writer(out)
    for key,value in Houses_Dict.items():
        writer.writerow([key, value])



#to read it back
    # with open('RIHousing.csv', 'rb') as out:
    #reader = csv.reader(out)
   # mydict = dict(reader)


#The difference in page 2 and 1 is two words added to the end

#https://www.zillow.com/homes/for_rent/Providence-RI-02903/house,condo,apartment_duplex,mobile,townhouse_type/58978_rid/41.853196,-71.359635,41.763245,-71.493702_rect/12_zm/

#https://www.zillow.com/homes/for_rent/Providence-RI-02903/house,condo,apartment_duplex,mobile,townhouse_type/58978_rid/41.853196,-71.359635,41.763245,-71.493702_rect/12_zm/2_p/

Houses = pandas.read_csv("RIHousing.csv")
print(Houses)
print(Houses.shape)
print(Houses.columns)


#with matplotlib we have the ability to plot data now
plt.hist(Houses['Rent'])
plt.show()

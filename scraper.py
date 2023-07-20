# https://www.samsclub.com/robots.txt states that this should be fine to scrape their website. If a rep from Sam's Club wants me to remove it, feel free to contact me and I will remove this
# https://www.bjs.com/robots.txt states that this should be fine to scrape their website. If a rep from BJs wants me to remove it, feel free to contact me and I will remove this

import setup
from bs4 import BeautifulSoup
import requests
import csv
import re
#get packages
print("Installing packages")  #TODO make setup an if statement
#setup.install()
#get html from website
print("Scraping URLs")  #TODO add if statement to check if we got a request, else print error
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/99.0", 
    "method": "GET"
}

#MIGHT NEED TO SCRAP SINCE SAMS CLUB NO LONGER ALLOWS BOTS TO USE /S/ PAGES
#samsURL = "https://www.samsclub.com/s/2055516?rootDimension=Tire%20Diameter%3A16%3A16%20in.pipsymbTire%20Aspect%20Ratio%3A55pipsymbTire%20Width%3A205%3A205%20in.%3A205%20mmpipsymbTire%20Season%3AAll%20Season&searchCategoryId=1056&sortKey=p_retail_sort&sortOrder=0&tireSearchTerm=205%2F55R16"
#page_to_scrape = requests.get(samsURL,headers=headers) 
#samSoup = BeautifulSoup(page_to_scrape.text, 'html.parser') 

bjsURL = "https://tires.bjs.com/tires/search/?width=205&aspect=55&rim=16&sort=price-asc&types=6&qty-filter=4"
page_to_scrape = requests.get(bjsURL,headers=headers)
bjSoup = BeautifulSoup(page_to_scrape.text, 'html.parser')

file = open('html.html','w')
file.write(str(bjSoup.prettify))
file.close()

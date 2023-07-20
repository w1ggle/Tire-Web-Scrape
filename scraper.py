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

bjsURL = "https://tires.bjs.com/tires/search/?width=205&aspect=55&rim=16&sort=price-asc&types=6&qty-filter=4&action=update&entity=4073"


page_to_scrape = requests.get(bjsURL,headers=headers)
bjSoup = BeautifulSoup(page_to_scrape.text, 'html.parser')

#file = open('html.html','w')
#file.write(str(bjSoup.prettify))
#file.close()


#tabulating
print("Tabulating data") 
file = open('output.csv', 'w')
writer = csv.writer(file)
writer.writerow(['Brand', 'Model', 'CPU', 'CPU Score', 'RAM (GB)', 'RAM Type', 'Storage (GB)', 'GPU', 'Size (In)', 'Color', 'Price ($)', 'Refurbed' , 'Open Box', 'Link' ]) #create CSV file

products = MicroSoup.findAll('div', attrs={"class":"result_right"}) #extracting data from each product
for product in products: 
    brand = model = cpu = score = ramCapacity = ramType = storage = gpu = price = refurbishedStatus = openBoxStatus = color = size = link = None #gpu is usually None but did the rest for safety
    
    link = 'https://www.microcenter.com' + product.find("a").get("href")
    brand = product.find("a").get("data-brand") 
    model = product.find("a").get("data-name") #example: ENVY x360 15-ey0013dx 15.6&quot; 2-in-1 Laptop Computer (Refurbished) - Black 

    index = model.rfind(' ')
    color = model[index+1:]
    
    if (model.find("Refurbished",index - 20) != -1):
        refurbishedStatus = "x"

    index = model.find(";")
    if(index == -1): #weird edge case 
        index = model.find("-in-1")
    model = model[:index]

    index = model.rindex(" ")+1
    size = model[index:].replace('&quot','')
    model = model[:index]
    
    priceWrapper = product.find("div", attrs={"class":"price_wrapper"})
    priceOpenBox = priceWrapper.find("div", attrs={"class":"clearance"}) 
    priceOpenBoxIndex = priceOpenBox.text.find("$") 
    if (priceOpenBoxIndex != -1):
        price = (priceOpenBox.text[priceOpenBoxIndex:]) 
        openBoxStatus = "x"
    else:
        price = (priceWrapper.find("span", attrs={"itemprop":"price"}).text) 
    price = price.replace(',', '').replace('$', '') #remove $ sign and , so that it sorts correctly
    
    fullSpecs = product.find("div", attrs={"class":"h2"}).text.split("; ") #example: HP ENVY x360 Convertible 15-eu1073cl 15.6" 2-in-1 Laptop Computer (Refurbished) - Black;  AMD Ryzen 7 5825U 2.0GHz Processor;  16GB DDR4-3200 RAM;  512GB Solid State Drive;  AMD Radeon Graphics
    for spec in fullSpecs[1:]:
        if(spec.find("Processor") != -1):
            cpu = spec[:-17]
            if(cpu.find("AMD") != -1):
                cpu = cpu[5:]
            else:
                index = cpu.rindex("i")
                cpu = cpu[index:]
                cpu = re.sub(" ..th Gen ","-",cpu)
            score = PassSoup.find("a", string=re.compile(cpu)).parent.parent.findAll("td")[1].text.replace(",","")
        elif(spec.find("RAM") != -1):
            ram = spec[1:-4] 
            index = ram.find("GB")
            ramCapacity = ram[:index]
            ramType = ram[index+3:]
        elif(spec.find("Solid State Drive") != -1):
            storage = spec[:-18].replace("TB","000").replace("GB","")
        elif(spec.find("AMD") != -1 or spec.find("Intel") != -1 or spec.find("NVIDIA") != -1 ):
            gpu = spec

    writer.writerow([brand, model, cpu,score, ramCapacity, ramType, storage, gpu, size, color, price, refurbishedStatus, openBoxStatus, link]) #TODO see if its possible to get ALL inventory and not just 96 results, add my own personal score/rating, make csv 2 sheets where 1 is for calulations and other is for front end

file.close() 
print("DONE! Check output.csv")
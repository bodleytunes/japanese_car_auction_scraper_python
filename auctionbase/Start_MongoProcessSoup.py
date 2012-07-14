'''
Created on 22 Nov 2011

@author: jon
'''
import subprocess
from main import start
import PostgresInserter



seleniumScrapeLocation = r"/home/jon/AuctionScraper/seleniumscrapevehicles/SeleniumTestMain/bin/SeleniumTestMain.exe"

def ProccessAndInsertDataToMongo():
    
    
    
    
    #Call the C# Selenium webscraper to scrape initial data to SQL Server.
    #subprocess.call([seleniumScrapeLocation])
    #Process Mongo DB with beautifulsoup and copy to mongo_web_page (still mongo)
    start.begin()
    
    #Insert to postgres
    PostgresInserter.Begin()
    
   


ProccessAndInsertDataToMongo()

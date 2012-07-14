'''
Created on 22 Nov 2011

@author: jon
'''
import subprocess
import PostgresInserter
from auctionsearch.main import start



seleniumScrapeLocation = r"C:\AuctionScraper\seleniumscrapevehicles\SeleniumTestMain\bin\Debug\SeleniumTestMain.exe"

def ProccessAndInsertDataToMongo():
    
    #Call the C# Selenium webscraper to scrape initial data to SQL Server.
    
    subprocess.call([seleniumScrapeLocation])
    #Process Mongo DB with beautifulsoup and copy to mongo_web_page (still mongo)
    start.begin()
    # delete all vehicles from the huge vehicles database on mongo
    start.delete_vehicles()
    
    #Insert to postgres
    PostgresInserter.Begin()
    
   


ProccessAndInsertDataToMongo()

'''
Created on 1 Feb 2012

@author: jon
'''
from auctionsearch.auctionbase import Start_MongoProcessSoup



def begin():
    Start_MongoProcessSoup.ProccessAndInsertDataToMongo()
    
begin()


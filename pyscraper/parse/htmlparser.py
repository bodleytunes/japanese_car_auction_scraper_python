from bs4 import BeautifulSoup
import sys

from model import *
from datetime import *

from sqlalchemy import *
from sqlalchemy import create_engine    
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct

vehicles_to_save = []


def start_parse(row_data, row_html, f,\
                 make, model, db, day_id, search_session_id):
    
    
    # now with the single web element use .text to get a string of the text items delimeted by newlines \n
    # then just split by the new lines to get the separate cells!
    # old way to get html (for parsing) 
    # (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableElement);
    #print(row_html)
    global soup
    soup = BeautifulSoup(row_html)
    #raw_input(soup.prettify())
    
    lotnumber = soup.find("a", { "class" : "my_bids" })
    lotnumber_text = lotnumber.string
    #raw_input("lotnumber = " + lotnumber_text)
    auction_house = soup.find_all("nobr")[1].string
    # got first half of auction house
    #print auction_house
    auction_house = auction_house.replace("\n","")  #remove newlines
    auction_house = auction_house.strip()           #remove whitespace
    lotnumber_text = lotnumber_text.replace("\n","")  #remove newlines
    lotnumber_text = int(lotnumber_text.strip())           #remove whitespace
    auction_dict = {"USS Nag" : "USS NAGOYA", \
                    "CAA Nag" : "CAA NAGOYA", \
                    }
    
  

    #raw_input(auction_house)
    #print auction_dict[auction_house]
    #auction_house = auction_dict[auction_house]
    
    # Get image and vehicle links
    img_link_list = soup.find_all("a", {"class": "aj_resize"})
    vehicle_link_list = soup.find_all("a", {"class" : "my_bids"})
    
    try:
        img1 = img_link_list[0]["href"]  # get correct indices and then href key
    except:
        print "img1 problem"
        img1 = None
    try:
        img2 = img_link_list[1]["href"]
    except:
        print "img2 problem"
        img2 = None
    try:
        img3 = img_link_list[2]["href"]
    except:
        img3 = None
        print "img3 problem"
    try:
        vehicle_link = vehicle_link_list[0]['href']
    except:
        print "vehicle link prob"
    
    # Save vehicle data
    save_vehicle_to_db(db,f, auction_house,lotnumber_text,vehicle_link,make,model,img1,img2,img3 \
                       ,search_session_id,day_id,None,None,None,None)
    #vehicles_to_save.append(vehicle(lotnumber,make,model,None,None,\
                 #None,None,None,None,img1,img2,img3,vehicle_link))
    
    # test save
    
   
    
    
    #//*[@id="aj_view3"]/td[4]    
        
    #raw_input("lotnumber = " + lotnumber_text)
    
   
    #f.write("lotnumber = " + lotnumber_text + "\n")
    #for link in soup.find_all('a'):
       # print(link.get('href'))
    
    #raw_input(row_data.text)
    #row_list = row_data.text.split("\n")
    #for item in row_list:
    #    print item
        
    #print "======================="
    
   
    #f.write("lotnumber = " + str(lotnumber_text) + " " + auction_house + "\n")
    #for link in soup.find_all('a'):
    #    print(link.get('href'))
    
    #raw_input(row_data.text)
    #row_list = row_data.text.split("\n")
    #for item in row_list:
    #    print item
        
    #print "======================="
    
   
    #return auction_house_unique

def save_vehicle_to_db(db,f, auctionHouse,lotNumber,remoteurl,make,model,imgurl1=None,imgurl2=None,imgurl3=None, \
                       searchSession_id=None,day_id=None,beenViewed=None,year=None,miles=None,chassis=None):
      #create new auction vehicle
          
    avehicle = AuctionVehicle()
    avehicle.auctionHouse = auctionHouse
    avehicle.lotNumber = lotNumber
    avehicle.year = year
    avehicle.miles = miles
    avehicle.chassis = chassis
    avehicle.imgurl1 = imgurl1
    avehicle.imgurl2 = imgurl2
    avehicle.imgurl3 = imgurl3
    avehicle.remoteurl = "http://www.jpcenter.ru/" + remoteurl
    avehicle.remoteurlfin = "http://www.jpcenter.ru/" + change_to_finish_url(remoteurl)
    #Set the search session foreign key
    avehicle.searchSession_id = searchSession_id
    avehicle.day_id = day_id
    avehicle.beenViewed = False
    try:
        avehicle.searchVehicle_id = get_model_id(db, make, model)
    except:
        insert_new_searchvehicle(db, make, model)
        avehicle.searchVehicle_id = get_model_id(db, make, model)
    
    try:
        # Add the object to the current session
        db.add(avehicle)
        # Save the object to the database!
        db.commit()
        print("!")
        
    except Exception as e:        
        print(".")
        #print e
        db.rollback()
        
def get_model_id(db, make, model):
 

    query = db.query(SearchVehicle.id)\
            .filter(and_(SearchVehicle.make==make, SearchVehicle.model==model))\
            .one()
            
    return query.id

def insert_new_searchvehicle(db, make, model):
        
    svehicle = SearchVehicle()
    svehicle.make = make
    svehicle.model = model
    
    db.add(svehicle)
    
    try:
        db.commit
    except:
        print "FOUND A DUPLICATE SEARCHVEHICLE"

def get_latest_searchday(db):
    #db = GetDB()
    searchDay = db.query(SearchDay.id).order_by(desc(SearchDay.id)).first()
    
    return searchDay.id

def change_to_finish_url(remoteurl):
    
    finish_url = remoteurl.replace("aj-", "st-")
    
    return finish_url        

class vehicle():
    
    def __init__(self,lotnumber=None,make=None,model=None,year=None,miles=None,\
                 grade=None,date=None,start_price=None,end_price=None,img_1=None,\
                 img_2=None,img_3=None,vehicle_link=None):
        
        self.lotnumber=lotnumber
        self.make=make
        self.model=model
        self.year=year
        self.miles=miles
        self.grade=grade
        self.date=date
        self.start_price=start_price
        self.end_price=end_price
        self.img_1 = img_1
        self.img_2 = img_2
        self.img_3 = img_3
        self.vehicle_link = vehicle_link
        
        
    
  
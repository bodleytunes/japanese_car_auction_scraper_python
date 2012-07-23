'''
Created on 1 Nov 2011

@author: jonny boy clayton
'''
#from BeautifulSoup import BeautifulSoup
from bs4 import BeautifulSoup
import pymongo
from pymongo import Connection
from Objects.WebPage import *
import re
from Mail.mailer import *
#from f import *
import datetime





### CLASS VARIABLES
###
myDb = 'jmcmongo'
vehicleTypeList = []
webPageList = []
totalVehiclesList = []
totalVehiclesPerModel = 0

###
def begin():
    
    
    connection = ConnectMongo()
    db = GetDb(connection)
    
    collection = GetCollection(db)
    collection2 = GetCollection2(db)
    GetListOfVehiclesToSearch(collection, collection2)
  
    searchSession = ReturnLatestSearchSession(collection)
    
    ProcessAllVehicles(collection, searchSession, collection2)
    DisplayWebPageList()
    #SendEmail()
    CloseMongo(db, connection)
    
def CloseMongo(db, connection):
    
    connection.disconnect()
    
    
   
    
def ConnectMongo():
    connection = Connection(myDb)
    return connection 
    
# Do stuff!
def GetDb(connection):
    db = connection.Auctionvehicles
    return db

def GetCollection(db):
    
    
    collection = db.vehicles
       
    return collection

def GetMongoWebPageCollection(db):
    
    collection = db.mongo_web_page
    return collection

def GetCollection2(db):
    collection2 = db.mongo_search_vehicle
    return collection2

def ReturnVehiclesAndCount(vehicleType, collection):
    
    vehicleCursor = collection.find( { "model" : vehicleType }).sort("_searchSession", pymongo.DESCENDING)
        
    for vehicle in vehicleCursor:
        print(vehicle['_searchSession'])
    
    print("Total rows returned : " + str(vehicleCursor.count()))
    
def GetListOfVehiclesToSearch(collection, collection2):
    #Get a DISTINCT list of vehicle models!
    #cursor = collection.find({}, {"make" : 1, "model" : 1}).distinct("model")
    
    cursor2 = collection2.find()
    
    
    for vehicle in cursor2:
        print(vehicle["make"] + " " + vehicle["model"])
        
    #Create the list of vehicles to search
    #for vehicle in cursor2:
        #vehicleTypeList.append(SearchVehicle(vehicle.make)) 
    
    #for vehicle in vehicleTypeList:
        #print vehicle.make + vehicle.model
    
        
    
      
        
      
    
def ReturnLatestSearchSession(collection):
    
    #Get latest search session by searching all, and ordering so highest first and 
    #limit to one.
    cursor = collection.find( {},{"_searchSession" : 1 }).sort("_searchSession", pymongo.DESCENDING).limit(1)
    
    for vehicle in cursor:
        print("Latest Search session number = " + str(vehicle['_searchSession']))
    
    print("Total rows returned : " + str(cursor.count()))
    
    searchSession = vehicle['_searchSession']
    
    return searchSession
 
def GetLatestVehiclesByModel(collection, searchSession, model):
    
    cursor = collection.find({ "model" : model, "_searchSession" : searchSession }, {"htmlData" : 0})
    
    i = 1
    for vehicle in cursor:
        print("Latest vehicles : " + str(i) + " " + str(vehicle)) 
        i += 1
        
    print("Total Vehicles = " + str(i-1) + " " + vehicle['model'])
    
def GetSingleHtml(collection):
    cursor = collection.find( { "model" : vehicleType },{"htmlData.htmlRow" : 1 }).sort("_searchSession", pymongo.DESCENDING).limit(1)
    
    
    # THIS DRILLS DOWN INTO COLLECTION TO GET ONLY THE EMBEDDED DATA!!! IMPORTANTO!
    message1 = "Getting single html row : "
    print(message1 + cursor[0]["htmlData"][0]["htmlRow"])
    message2 = "Processing single html row ***"
    
    htmlString = str(cursor[0]["htmlData"][0]["htmlRow"])
    # Process the html with Beautiful Soup.
    ProcessHtml(htmlString)

def ProcessAllVehicles(collection, searchSession, collection2):
    totalVehicles = 0
    global totalVehiclesPerModel
    #totalVehiclesPerModel = 0
    
    cursor3 = collection2.find()
    
    for vehicleType in cursor3:
        totalVehiclesPerModel = 0
        GetAllHtml(collection, vehicleType["model"], searchSession, totalVehicles, vehicleType["make"], vehicleType["model"])
        #Print total number of models found and added (NEW)
        print("total " + vehicleType["model"] + " " + "added = " + str(totalVehiclesPerModel))
        #raw_input("Continue...")
        # Now write the total vehicles (per model) to collection
    
    
        
def GetAllHtml(collection, vehicleType, searchSession, totalVehicles, currentMake,currentModel):
    
    cursor = collection.find( { "model" : vehicleType, "_searchSession" : searchSession },{"htmlData.htmlRow" : 1}).sort("_searchSession", pymongo.DESCENDING)
    
    # Fails if you try and proceed with nothing in the cursor
    if cursor.count() > 0:
        
        # THIS DRILLS DOWN INTO COLLECTION TO GET ONLY THE EMBEDDED DATA!!! IMPORTANTO!
        message1 = "Getting all html row(s) : "
        print(message1 + cursor[0]["htmlData"][0]["htmlRow"],currentMake)
        #message2 = "Processing single html row ***"
        
        #htmlString = str(cursor[0]["htmlData"][0]["htmlRow"])
        for vehicle in cursor:
            
            ProcessHtml(vehicle["htmlData"][0]["htmlRow"],currentMake,currentModel)
            
            totalVehicles += 1
            
            
    # Process the html with Beautiful Soup.
   # ProcessHtml(htmlString)
    

def ProcessHtml(html, make, model):
    
    ## Check HTML for the fcurr* tag if not exists then skip this lot!
    soup = BeautifulSoup(html)
    #find_string_check = re.findall('(Fcurr)', html)
    #find_string_check = soup.findAll('span', attrs={"id":"Fcurr*"})
##    find_string_check = soup.findAll('span', attrs={"id": re.compile('^Fcurr')})
##    #re.compile('l[0-9]*')
##    # If the count of the number of strings is zero, then skip / exit early.
##    if len(find_string_check) < 1:
##        print("cant find fcurr !!!!!")
##        return
    
    #Create a new web page object
    webpage = WebPage()
    webpage.make = make
    webpage.model = model
        
    # Call beautifulsoup and send html to it.
    print("calling beautiful soup")
    #raw_input(html)

    bs = BeautifulSoup(html)
    
    urls = bs.findAll(href=True)
    
    urlList = []
   
    
    
    for result in urls:
        print("found URL : " + result['href'])
        urlList.append(result['href'])
    try:
        webpage.imgurl1 = urlList[0] 
    except:
        print "problem with url 0"
        
    try:
        webpage.imgurl2 = urlList[1]
    except:
        print "problem with url 1"
        
    try:
        webpage.imgurl3 = urlList[2]
    except:
        print "problem with url 2"
        
        
    try:
        webpage.remoteUrl = "http://www.jpcenter.ru/" + urlList[3]  
    except:
        print "problem with url 2"
    
    
    print(webpage.imgurl1)
    print(webpage.imgurl2)
    print(webpage.remoteUrl)
    
    lotData = bs.findAll('center')
           
    print(lotData[0].text)
    lotnumber = lotData[0].text
    # Now use a regex to extract the number from the garbage
    lotnum = re.search(r'(\d+)', lotnumber)
    # Get the matched string out of the matched regex
    if lotnum != None:
        lotnum = lotnum.group()
        print("lotnumber = " + lotnum)
    else:
        lotnum = None
    
    
    webpage.lotnumber = lotnum
    
    yearData = bs.findAll(name="span", style=re.compile("color:#a93f15"))
    #extract the text part of html
    if yearData != None:
        
        try:
            year = yearData[0].text
        #extract the year using a regex to find four digits
            year = re.search(r'[0-9]{4}', year)
     
        except:
            print "problem with year data"
       
    try:
        year = year.group()
    except:
        year = ""
        pass
    
    #Use string replace to remove the year from the string
    try:
        chassis = str.replace(str(yearData[0].text),year, "")
    except:
        print "found dodgy unicode!"
        chassis = None
    
    print ("Year is : " + year)
    
    try:
        print ("Chassis is : " + chassis)  
    except:
        print "no chassis"
    
    
    webpage.year = year
  
    webpage.chassis = chassis
        
    
    auctionHouseData = bs.findAll(name="span", style=re.compile("font-size:10px;color:#ccc"))
    #auctionHouseText = auctionHouseData[0].text
    print(auctionHouseData)
    #regex = re.search(r'[0-9]{4}', str(auctionHouseText))
    #regex = regex.group()
    
    
    #print(regex)
    
    #auctionHouse = str.replace(str(auctionHouseData[0].text),regex,"")
    
    try:
        auctionHouse = auctionHouseData[0].text
        regEx = re.search(r':[0-9]{4}', auctionHouse)
    except:
        print "problem with auction house data"
    
   
    try:
        regEx = regEx.group()
        print("Auction House OK!")
        newAuctionHouse = str.replace(str(auctionHouse),str(regEx),"")
    except:
        regEx = ""
        print("Auction House Exception!")
        newAuctionHouse = auctionHouse
        pass
    
    
    
    print("Auction house is : " + newAuctionHouse)
    
    webpage.auctionHouse = newAuctionHouse
    
    #Get prices
    
    priceData = bs.findAll(name="div", style="display:none", id=(re.compile("Fcurr")))
    # just get the text
    priceDataText = priceData[0].text
    # now replace the bit you dont want
    priceDataText = str.replace(str(priceDataText), "yen|0|0|", "")
    
    print(priceDataText)
    webpage.price = priceDataText
   
    # Write the webpage to list
    WriteToWebPageList(webpage)
    # Write the webpage to the Mongo Database
    MongoOps(webpage)
    
    
def WriteToWebPageList(webpage):
    
    webPageList.append(webpage)
    
    

    
def MongoOps(webpage):
    
    #Get the date
    #dt = datetime()
    date = datetime.datetime.now()
    global totalVehiclesPerModel    
    
        
    print "Saving Vehicle WebPage Data to MONGO DB"
    db = connect('Auctionvehicles',host='jmcmongo')
    
    mongoPage = MongoWebPage()
    mongoPage.make = webpage.make
    mongoPage.model = webpage.model
    mongoPage.auctionHouse = webpage.auctionHouse
    mongoPage.lotnumber = webpage.lotnumber
    mongoPage.chassis = webpage.chassis
    mongoPage.year = webpage.year
    mongoPage.cc = webpage.cc
    mongoPage.imgurl1 = webpage.imgurl1
    mongoPage.imgurl2 = webpage.imgurl2
    mongoPage.imgurl3 = webpage.imgurl3
    mongoPage.remoteUrl = webpage.remoteUrl
    mongoPage.dateAdded = date
    mongoPage.price = webpage.price
    mongoPage.postgresExport = False
    
    #Check for dupes before saving
    dupeAlert = MongoCheckDupes(webpage)
    try:
        if dupeAlert == 0:
            mongoPage.save()
            totalVehiclesPerModel+= 1
    except:
        print("not written!")
    finally:
        print("continuing")
        
    db.disconnect()
    
    
    
        
        
def MongoCheckDupes(webpage):
    
    #Connect to DB again
    connection = ConnectMongo()
    db = GetDb(connection)
    collection = GetMongoWebPageCollection(db)
    #query to check if imgurl's (unique) already exist
    cursor = collection.find( {"imgurl1" : webpage.imgurl1, "imgurl2" : webpage.imgurl2 } )
    
    for item in cursor:
        print(item)
    
    print(cursor.count())
    print(webpage.imgurl1)
    #raw_input("continue?")
    
    if cursor.count() > 0:
        print("FOUND DUPES - RETURNING 1")
        #raw_input("continue?")
        #disconnect socket from db
        # changed from connection.disconnect() will see how this goes?
        connection.disconnect()
        return 1
    
    else:
        
        #raw_input("continue?")
        connection.disconnect()
        return 0
    
    connection.disconnect()
    
   
     
    
        
    
        
        
    
    
    
    
    


    
    
    
    
def DisplayWebPageList():

    
    for page in webPageList:
        try:
            
            print("*****VEHICLE DETAILS*****")
            print("Image1 : " + page.imgurl1)
            print("Image2 : " + page.imgurl2)
            print "Remote URL : " + page.remoteUrl 
            print "Lot Number : " + page.lotnumber 
            print "Vehicle Year : " + page.year 
            print "Vehicle CC : " + str(page.cc) 
            print "Vehicle Mileage (KM) : " + str(page.mileage) 
            print "Vehicle Price : " + str(page.price) 
            print "Vehicle Chassis Type : " + str(page.chassis) 
            print "Vehicle Auction House : " + str(page.auctionHouse)
            print "Supercamper Number : " + str(page.superCamperNumber)
            print ("***********BREAK**********")
            print ("***********BREAK**********")
        except:
            print "problem with text and nonetype!"

def delete_vehicles():
    
    connection = ConnectMongo()
    db = GetDb(connection)
    
    collection = GetCollection(db)
    
    collection.remove()
    

def bstest():
    html = "<span id=""Fcurr0233"">"
    bs = BeautifulSoup(html)
    find_string_check = bs.findAll('span', attrs={"id": re.compile('^Fcurr')})
    print find_string_check

#delete_vehicles()

           
#bstest()   
#begin()
    

    

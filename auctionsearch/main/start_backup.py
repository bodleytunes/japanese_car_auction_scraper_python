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
    #ReturnVehiclesAndCount(vehicleTypeList,collection)
    searchSession = ReturnLatestSearchSession(collection)
    #GetLatestVehiclesByModel(collection,searchSession,vehicleTypeList)
    #GetSingleHtml(collection)
    #GetAllHtml(collection)
    ProcessAllVehicles(collection, searchSession, collection2)
    DisplayWebPageList()
    SendEmail()
    
    
   
    
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
    
    cursor = collection.find( { "model" : vehicleType, "_searchSession" : searchSession },{"htmlData.htmlRow" : 1 }).sort("_searchSession", pymongo.DESCENDING)
    
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
    
    #Create a new web page object
    webpage = WebPage()
    webpage.make = make
    webpage.model = model
        
    # Call beautifulsoup and send html to it.
    print("calling beautiful soup")
    
    bs = BeautifulSoup(html)
    
    urls = bs.findAll(href=True)
    
    urlList = []
   
    
    
    for result in urls:
        print("found URL : " + result['href'])
        urlList.append(result['href'])
    
    webpage.imgurl1 = urlList[0]
    webpage.imgurl2 = urlList[1]
    webpage.remoteUrl = "http://www.jpcenter.ru/" + urlList[2]
    
    print(webpage.imgurl1)
    print(webpage.imgurl2)
    print(webpage.remoteUrl)
    
    lotData = bs.findAll('center')
           
    print(lotData[0].text)
    lotnumber = lotData[0].text
    # Now use a regex to extract the number from the garbage
    lotnum = re.search(r'(\d+)', lotnumber)
    # Get the matched string out of the matched regex
    lotnum = lotnum.group()
    print("lotnumber = " + lotnum)
    
    webpage.lotnumber = lotnum
    
    yearData = bs.findAll(name="span", style=re.compile("color:#a93f15"))
    #extract the text part of html
    year = yearData[0].text
    #extract the year using a regex to find four digits
    year = re.search(r'[0-9]{4}', year)
    
    try:
        year = year.group()
    except:
        year = ""
        pass
    
    #Use string replace to remove the year from the string
    chassis = str.replace(str(yearData[0].text),year, "")
        
    print ("Year is : " + year)
    
    print ("Chassis is : " + chassis)
    
    webpage.year = year
    webpage.chassis = chassis
    
    auctionHouseData = bs.findAll(name="span", style=re.compile("font-size:10px;color:#ccc"))
    #auctionHouseText = auctionHouseData[0].text
    print(auctionHouseData)
    #regex = re.search(r'[0-9]{4}', str(auctionHouseText))
    #regex = regex.group()
    
    
    #print(regex)
    
    #auctionHouse = str.replace(str(auctionHouseData[0].text),regex,"")
    auctionHouse = auctionHouseData[0].text
    
    regEx = re.search(r':[0-9]{4}', auctionHouse)
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
    
    webpage.postgresExport = 
   
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
    mongoPage.remoteUrl = webpage.remoteUrl
    mongoPage.dateAdded = date
    mongoPage.price = webpage.price
    
    
    #Check for dupes before saving
    dupeAlert = MongoCheckDupes(webpage)
    
    if dupeAlert == 0:
        mongoPage.save()
        totalVehiclesPerModel+= 1
        
        
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
        connection.disconnect()
        return 1
    
    else:
        
        #raw_input("continue?")
        return 0
   
     
    
        
        
        
    
    
    
    
    


    
    
    
    
def DisplayWebPageList():

    
    for page in webPageList:
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
        
def SendEmail():
    
    message = Message()
    message.From = "SC_Python_Auctions@supercamper.co.uk"
    message.To = "supertent@gmail.com"
    message.Subject = "Automatic Vehicle Finder Results"
    message.Body = "test "
    message.Html = """This email is in <b>HTML</B>.<a href="http://www.supercamper.co.uk">Here's a link.</a>"""
   
    mailer = Mailer("mailex")
    mailer.send(message)



        
   
#begin()
    

    
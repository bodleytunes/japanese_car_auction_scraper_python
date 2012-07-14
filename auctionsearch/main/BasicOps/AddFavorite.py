'''
Created on 7 Nov 2011

@author: jon
'''

'''
Created on 7 Nov 2011


@author: jon
'''

'''
Created on 6 Nov 2011

@author: jon
'''

import pymongo
from pymongo import Connection
from mongoengine import *
from WebPage import *
import datetime


def AddFaveBegin():
    inputdata = ""
    inputdata = raw_input("Do you want to add a favourite?")
    if inputdata == "y" or inputdata == "Y":
            print("playing get input")
            GetInput()
            AddFaveBegin()
            
    elif inputdata == "n":
        exit
    else:
        AddFaveBegin()
        
   
        
   

def GetInput():
    connect("Auctionvehicles",host="jmcmongo")
    
    userVehicleFavorite = UserVehicleFavorite()
    name = getName()
   
    
    vehicle = getVehicle()
    
    
    userVehicleFavorite.favoriteDate = datetime.datetime.now()
    
        
    #
    userVehicleFavorite.userId = name
    userVehicleFavorite.vehicleId = vehicle
    
    print("User ID = " + str(name))
    print("vehicle ID = " + str(vehicle))
    
    raw_input("continue saving?")
    
    #try:
    userVehicleFavorite.save()
    print("Saved to DB...")
#except:
    #print "duplicate - not saved"
    #pass
    
   
    
def getName():
    input = raw_input("Enter name: ")
    
    if input == "":
        print("enter something please")
        getName()
        
    #query name
    idName = queryName(input)
    
        
    return idName


        
    
        
def getVehicle():
    input = raw_input("Enter vehicle lotnumber: ")
    
    if input == "":
        print("enter something please")
        getVehicle()
        
     #query vehicle
    vehicleId = QueryVehicle(input)
    
        
    return vehicleId

def queryName(input):
    conn = ConnectMongo()
    db = GetDb(conn)
    collection = getCollection(db, "mongo_user")
    
    cursor = collection.find( {"userName" : input} )
    if cursor.count() > 0:
        
        #user = MongoUser()
        user = cursor[0]["_id"]
        
        print("found this id : " + str(user))
        raw_input("continue")
        
        return user
    
    
    raw_input("Couldn't find the user")
    AddFaveBegin()
    
def QueryVehicle(input):
    conn = ConnectMongo()
    db = GetDb(conn)
    collection = getCollection(db, "mongo_web_page")
    
    cursor = collection.find( {"lotnumber" : input} )
    if cursor.count() > 0:
    
        #vehicleWebPage = MongoWebPage()
        
        vehicleWebPage = cursor[0]["_id"]
        
        print("found this id : " + str(vehicleWebPage))
        raw_input("continue")
        
        return vehicleWebPage
    
    
    raw_input("Couldn't find the lotnumber")
    AddFaveBegin()
    
    

def ConnectMongo():
    connection = Connection("jmcmongo")
    return connection 
    
# Do stuff!
def GetDb(connection):
    db = connection.Auctionvehicles
    return db
    
def getCollection(db, collection):
    
    if collection == "mongo_web_page":
        collection = db.mongo_web_page
        return collection
    
    if collection == "mongo_user":
        collection = db.mongo_user
        return collection
    
    
AddFaveBegin()    
    
    


    


    
        
    








'''
Created on 22 Nov 2011

@author: jon
THIS COMES AFTER PROCESSING THE DATA WITH SOUP AND INSERTING INTO MONGO
THIS WILL INSERT THE CLEAN DATA INTO POSTGRES (AUCTIONBASE)
'''

import query
import re
import pymongo
from pymongo import Connection
from datetime import date, datetime
from datetime import timedelta
from mailer import *

emailList = ["supertent@gmail.com", "radio5mike@gmail.com"]


def DailyStatsAndEmail():
    #Insert session results to searchstat table
    query.SearchStatOps()
#Insert totals into the Day Totals table
    query.DayTotalOps()
    
    htmlBody1 = query.PrintSearchSessionTotals()
#Print the totals for the day
    #htmlBody3 = str(htmlBody1) + str(htmlBody2)
#Semd the results email
    #EmailOps(htmlbody1)
    

def Begin():
    
    mongoCursor = query.initalMongoOps()
    
    count = mongoCursor.count()
    print(str(count) + " Total vehicles in Mongo")
        
    VehicleOps(mongoCursor)
    
    DailyStatsAndEmail()

    
    
def RemoveNoneNumericCharacters(string):
    
    newValue = re.sub(r"\D", "", string)
    
    return newValue
    

def InsertAndGetNewSearchSession():
    
   
    #Insert new search session
    newdate = datetime.now()
    #Round time to nearest day by getting rid of the unwanted shizzle
    #Dont round this any more as will do this for the day session
    #newdate = newdate.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
      
    
    
    print(newdate)
    
    
    query.InsertSearchSession(newdate)
    #Select new search session
    searchSession = query.QgetLatestSearchSession()
    
    return searchSession

def InsertAndGetNewSearchDay():
    
    newDay = datetime.now()
    # Round to nearest day
    newDay = newDay.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    
    #get day from date
    dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    actualDay = dayofWeek[date.weekday(newDay)]
    
   
    
    query.InsertSearchDay(newDay, actualDay)
    
    dayId = query.QgetLatestSearchDay()
    
    return dayId

def VehicleOps(mongoCursor):
    
    searchSession = InsertAndGetNewSearchSession()
    dayId = InsertAndGetNewSearchDay()
    #get a new db session to do the updating
    db = query.GetMongoDb()
    
    #raw_input("the day id is " + str(dayId))
    
    
    
    for vehicle in mongoCursor:
        # This is where we do the honours, iterate through the mongo cursor and insert to postgres.
        print("Inserting to Postgres DB")
        
        # This to check for ones without years and change to 1990
        if vehicle["year"] == "":
            vehicle["year"] = 1990
        
        query.InsertVehicle(vehicle["auctionHouse"],\
                            RemoveNoneNumericCharacters(vehicle["lotnumber"]),\
                            vehicle["year"],\
                            None,\
                            vehicle["chassis"],\
                             vehicle["imgurl1"],\
                              vehicle["imgurl2"],\
                               None,\
                                vehicle["remoteUrl"],\
                                vehicle["make"],\
                                 vehicle["model"],\
                                  searchSession,\
                                  dayId)
        print("Insert Success!")
        
        # Now mark the exported column to true so it isn't exported again
        #print(vehicle["_id"])
        #raw_input("id is above")
        
        searchId = vehicle["_id"]
        
        #Use the find and modify command thin wrapper (pymongo) to query for vehicle then update it.
        #db.command("findandmodify", "mongowebpage", query={"_id": searchId}, update={"$set" : {"postgresExport" : "true" }})
        db.find_and_modify(query={"_id" : searchId}, update={"$set" : {"postgresExport" : True }})
       
    
    print("INSERTING INTO POSTGRES IS NOW FINITO")
    
def EmailOps(messageBody):
    
    global emailList
    
    for user in emailList:
        
        SendEmail(user, messageBody)
    
    
def SendEmail(user, messageBody):
       
        
    message = Message()
    message.From = "SC_Auctions@supercamper.co.uk"
    message.To = user
    message.Subject = "Automatic Vehicle Finder Results"
    #message.Body = messageBody
    message.Html = messageBody
   
    mailer = Mailer("mailex")
    mailer.send(message)
    
#InsertAndGetNewSearchDay()

#DailyStatsAndEmail()
    
    
#Begin()
#InsertAndGetNewSearchDay()
# query.DayTotalOps()


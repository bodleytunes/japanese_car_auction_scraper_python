'''
Created on 22 Nov 2011

@author: jon
THIS COMES AFTER PROCESSING THE DATA WITH SOUP AND INSERTING INTO MONGO
THIS WILL INSERT THE CLEAN DATA INTO POSTGRES (AUCTIONBASE)
'''
import sys
import query
import re
import pymongo
from pymongo import Connection
from datetime import date, datetime
from datetime import timedelta
from mailer import *
import time
#from webstuff import emailer

sys.path.append("F:\Documents and Settings\jon.JMC\My Documents\Aptana Studio 3 Workspace\MyWeb\src\webstuff")
import emailer



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
            
        # Create the URL for the finished vehicle (sold / not sold etc)
        remoteurlfin = ChangeUrlToFinishedUrl(vehicle["remoteUrl"])
        try:
            query.InsertVehicle(vehicle["auctionHouse"],\
                            RemoveNoneNumericCharacters(vehicle["lotnumber"]),\
                            vehicle["year"],\
                            None,\
                            vehicle["chassis"],\
                             vehicle["imgurl1"],\
                              vehicle["imgurl2"],\
                               None,\
                                vehicle["remoteUrl"],\
                                remoteurlfin,\
                                vehicle["make"],\
                                 vehicle["model"],\
                                  searchSession,\
                                  dayId)
        except:
            print "error inserting!!!!!!!!!!!! Possible key error?"
        
        print("Insert Success!")
        
        # Now mark the exported column to true so it isn't exported again
        #print(vehicle["_id"])
        #raw_input("id is above")
        
        searchId = vehicle["_id"]
        
        #Use the find and modify command thin wrapper (pymongo) to query for vehicle then update it.
        #db.command("findandmodify", "mongowebpage", query={"_id": searchId}, update={"$set" : {"postgresExport" : "true" }})
        db.find_and_modify(query={"_id" : searchId}, update={"$set" : {"postgresExport" : True }})
       
    
    print("INSERTING INTO POSTGRES IS NOW FINITO")
    
    #close connection to mongo db
    query.CloseMongoDb()
    
    # Check data for custom Alert e-mails to be sent out if need be.
    query.CustomAlertRoutine()
    
    # Now send emails
    GetModelIdSendEmails()
    
    print_date_completed()
    
def GetModelIdSendEmails():
    
    vehicle_id_list = query.GetAllVehiclesReturnsIds()
    
    for vehicle_id in vehicle_id_list:
        
        #raw_input("vehicle id about to send email for is" + str(vehicle_id[0]))
        #send an email - remember the id returned is a named tuple rather than an int, hence below...!
        #raw_input("vehicle id is now ... " + str(vehicle_id))
        emailer.send_html_email(vehicle_id[0])
    
    
def ChangeUrlToFinishedUrl(remoteurl):
     
    # Replace the string "/aj-" with "/st-" to get the final sale price url
    remoteurlfin = str.replace(str(remoteurl),"/aj-", "/st-")
    
    return remoteurlfin

def print_date_completed():
    
    print "Successfull FULL Scrape @ " + str(time.time()) + " "  + str(date.today())
    

#print_date_completed()

    
#def EmailOps(messageBody):
#    
#    global emailList
#    
#    for user in emailList:
#        
#        SendEmail(user, messageBody)
    
    
#def SendEmail(user, messageBody):
#       
#        
#    message = Message()
#    message.From = "SC_Auctions@supercamper.co.uk"
#    message.To = user
#    message.Subject = "Automatic Vehicle Finder Results"
#    #message.Body = messageBody
#    message.Html = messageBody
#   
#    mailer = Mailer("mailex")
#    mailer.send(message)
#    
#GetModelIdSendEmails()

#InsertAndGetNewSearchDay()

#DailyStatsAndEmail()
    
    
#Begin()
#InsertAndGetNewSearchDay()
# query.DayTotalOps()


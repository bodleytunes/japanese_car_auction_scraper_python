'''
Created on 22 Nov 2011

@author: jon
'''
 

from model import *
from datetime import *

from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker

from main import start


def Begin():
    
    collection = GetMongoDb()
    GetAllMongoVehicles(collection)
    
def initalMongoOps():
    collection = GetMongoDb()
    mongoCursor = GetAllMongoVehicles(collection)
    
    return mongoCursor
 
        
    
def GetMongoDb():
    
    mongoConn = start.ConnectMongo()
    mongodb = start.GetDb(mongoConn)
    collection = start.GetMongoWebPageCollection(mongodb)
    
    return collection



def GetAllMongoVehicles(collection):
    
    cursor = collection.find({"postgresExport" : False})
      
    return cursor
    
     

def GetDB():
    db = alchemysession
    
    return db
    
def QgetAllVehicles():
    
    db = GetDB()
    
    query = db.query(AuctionVehicle).all()
    
    print(query)
    print(query[0].lotNumber)
    
    return query

def QgetAllSearchVehicles():
    
    db = GetDB()
    
    query = db.query(SearchVehicle).all()
    
       
    return query

def GetMake(model):
    
    
    
    db = GetDB()
    
    query = db.query(SearchVehicle)\
            .filter(SearchVehicle.model == model)\
            .first()
    
       
    return query.make

def GetLatestDay():
    
    db = GetDB()
    
    query = db.query(SearchDay).order_by(desc(SearchDay.id)).first()
    
    day_id = query.id
    
    return day_id

def FavouriteOps(interestedVehiclesCursor, user_id):
    
    for vehicle in interestedVehiclesCursor:
        InsertFavourite(GetLatestDay(), vehicle.id, user_id)

def InsertFavourite(latestDay, auctionVehicleId, userId):
    
    db = GetDB()
    
    fave = Favourite()
    fave.auctionvehicle_id = auctionVehicleId
    fave.day_id = latestDay
    fave.user_id = userId
    
    db.merge(fave)
    try:
        db.commit() 
        print("Inserted new favourite")
    except exc.SQLAlchemyError:
        db.rollback()
        print("found dupes")
        
def GetAllUsers():
    
    db = GetDB()
    
    users = db.query(User).all()
    
    return users

    
        
def GetAllFavouritesToday(userId=None, dayId=None):
    
    if not userId:
        userId = 2
    if not dayId:
        dayId = GetLatestDay()
    
    db = GetDB()
    
    query = db.query(AuctionVehicle)\
            .join(Favourite.auctionvehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(and_(Favourite.day_id == dayId, Favourite.user_id == userId))\
            .all()
            
    for item in query:
        print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
        #print (str(item.id) + " " + str(item.day_id))    
        
 
    return query

#def GetAllFavouritesAll(userId=None, dayId=None):
def GetAllFavouritesAll():
    if not userId:
        userId = 2
#    if not dayId:
#        dayId = GetLatestDay()
    
    db = GetDB()
    
    query = db.query(AuctionVehicle)\
            .join(Favourite.auctionvehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(Favourite.user_id == userId)\
            .all()
            
    for item in query:
        print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
        #print (str(item.id) + " " + str(item.day_id))    
        
 
    return query

def GetAllFavouritesByModel(model):
    
#===============================================================================
#    if not userId:
#        userId = 2
# #    if not dayId:
# #        dayId = GetLatestDay()
#===============================================================================
    
    db = GetDB()
    
    query = db.query(AuctionVehicle)\
            .join(Favourite.auctionvehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(SearchVehicle.model == model)\
            .all()
            
    for item in query:
        print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
        #print (str(item.id) + " " + str(item.day_id))    
        
 
    return query
    

    
     

def DayTotalOps():
    
    query = QgetAllSearchVehicles()
    
    for searchVehicle in query:
        
        #Do the totals!
        DayTotal_Insert(searchVehicle.model)
    

def DayTotal_Insert(searchVehicle):
    
    # Practise changing this amount below to see if it works.    
    #newTotal = 361
    
    # Get Total for this vehicle
    newTotal = QgetTotalVehiclesToday(searchVehicle)
    
    db = GetDB()
    
    # Get current day.
    currentDay = QgetLatestSearchDay()
    
    dt = Day2SearchVehicle()
    
    # Get Vehicle ID
    vehicleId = db.query(SearchVehicle.id)\
            .filter(SearchVehicle.model == searchVehicle)\
            .first()
            
    
    
    dt.searchvehicle_id = vehicleId
    dt.day_id = currentDay
    dt.totalvehicles = newTotal
       
    db.merge(dt)
    
    try:
        db.commit() 
        print("Inserted new day total")
    except exc.SQLAlchemyError:
        db.rollback()
        print("found day dupes")
        # Now do an update rather than in insert
        DayTotal_Update(vehicleId, currentDay, newTotal)

def DayTotal_Update(searchVehicle, day_id, newTotal):
    
    # THIS IS HOW TO UPDATE SOMETHING !!!
    
    db = GetDB()
    
    db.query(Day2SearchVehicle)\
    .filter(and_(Day2SearchVehicle.searchvehicle_id == searchVehicle, Day2SearchVehicle.day_id== day_id))\
    .update({Day2SearchVehicle.totalvehicles : newTotal})
    
    db.commit()
    
def PrintSearchSessionTotals():
    
    searchVehicles = QgetAllSearchVehicles()
    ssId = QgetLatestSearchSession()
                                 
    db = GetDB()
    htmlBody = ""
    
    print ("*** SEARCH SESSION TOTALS ***")
    
    for searchVehicle in searchVehicles:
        
        print (searchVehicle.make + " " + searchVehicle.model)
        
        total = db.query(AuctionVehicle)\
                .filter(and_(AuctionVehicle.searchSession_id == ssId, AuctionVehicle.searchVehicle_id == searchVehicle.id))\
                .count()
                
        print ("Total today = " + str(total))
        
        htmlBody = htmlBody + str(generateMessageBody(str(total), searchVehicle.make, searchVehicle.model))
        
    
    
    return htmlBody


        
def generateMessageBody(total, make, model):
    
    htmlBody = "VEHICLE <br>" + make + " " + model + " <br>"
    htmlBody += "Total today = " + str(total) + " <br>"
    htmlBody += "************************************* <br>"
    
    return htmlBody

       
        
def PrintDayTotalResults():
    
    searchVehicles = QgetAllSearchVehicles()
    day_id = QgetLatestSearchDay()
    htmlBody = ""
                                 
    db = GetDB()
    
    print ("*** DAY TOTALS ***")
    
    for searchVehicle in searchVehicles:
        
        print (searchVehicle.make + " " + searchVehicle.model)
        
        total = db.query(Day2SearchVehicle.totalvehicles)\
                .join(Day2SearchVehicle.searchvehicle)\
                .filter(and_(Day2SearchVehicle.day_id == day_id, SearchVehicle.model == searchVehicle.model))\
                .first()
        print ("Total today = " + str(total))
        
        
        
        htmlBody = htmlBody + str(generateMessageBody(str(total.totalvehicles), searchVehicle.make, searchVehicle.model))
        
    return htmlBody
                
        
    
    

def QgetModelId(make, model):
    
    db = GetDB()

    query = db.query(SearchVehicle.id)\
            .filter(and_(SearchVehicle.make==make, SearchVehicle.model==model))\
            .one()
            
    return query.id

  
def InsertVehicle(auctionHouse=None,\
                  lotNumber=None,\
                  year=None,\
                  miles=None,\
                  chassis=None,\
                  imgurl1=None,\
                  imgurl2=None,\
                  imgurl3=None,\
                  remoteurl=None,\
                  make=None,\
                  model=None,\
                  searchSession=None,\
                  dayId=None):
    
    #get DB session
    db = GetDB()
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
    avehicle.remoteurl = remoteurl
    #Set the search session foreign key
    avehicle.searchSession_id = searchSession
    avehicle.day_id = dayId
    try:
        avehicle.searchVehicle_id = QgetModelId(make, model)
    except:
        InsertSearchVehicle(make, model)
        avehicle.searchVehicle_id = QgetModelId(make, model)
    
    try:
        # Add the object to the current session
        db.add(avehicle)
    # Save the object to the database!
        db.commit()
    except:        
        print("DUPLICATE IN POSTGRES!")
        db.rollback()
        
def InsertSearchVehicle(make=None, model=None):
    db = GetDB()
    
    svehicle = SearchVehicle()
    svehicle.make = make
    svehicle.model = model
    
    db.add(svehicle)
    
    try:
        db.commit
    except:
        print "FOUND A DUPLICATE SEARCHVEHICLE"
    
    
def QgetAllVehiclesByModel(model):
    db = GetDB()
    # Nice example of join query.
    query = db.query(AuctionVehicle)\
    .join(AuctionVehicle.searchVehicle)\
    .filter(SearchVehicle.model==model)\
    .all()
    
    # Return joined data
    for item in query:
        print(item.auctionHouse + " " + item.searchVehicle.make)
    
    return query

def QgetTotalVehiclesToday(searchVehicle):
    
    day_id = QgetLatestSearchDay()
    
    db = GetDB()
    
    #raw_input(day_id)
    
    queryTotal = db.query(AuctionVehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(and_(SearchVehicle.model == searchVehicle, AuctionVehicle.day_id == day_id))\
            .count()
            
    #raw_input(queryTotal)
    
    return queryTotal
    
    

def QgetInterestedCustomersByModel(model):
    
    db = GetDB()
    
    emailQuery = db.query(Customer)\
                .join(Customer2searchVehicle.customer, Customer2searchVehicle.searchvehicle)\
                .filter(SearchVehicle.model==model)\
                .all()
                
    return emailQuery

def QgetInterestingVehiclesForCustomersByModel(model):
    
    db = GetDB()
    
    interestedParties = QgetInterestedCustomersByModel(model)
    
    # Now get the latest vehicles by latest session id.

    for customer in interestedParties:
        print(customer.name + " " + customer.emailAddress)
        
        # Now get a list of the vehicles of interest for that customer
        truckData = db.query(AuctionVehicle)\
                .join(Customer2searchVehicle.customer, Customer2searchVehicle.searchvehicle, SearchVehicle.auctionVehicles)\
                .filter(AuctionVehicle.flagToSendEmail==True)\
                .filter(SearchVehicle.model==model)\
                .filter(SearchSession.id == QgetLatestSearchSession())\
                .all()
    
           
            ### SEND INDIVIDUAL TRUCK DETAILS AS EMAIL TO THE INTERESTED PARTY!!!
            
            

def QgetLatestSearchSession():
    # Get latest searchsession ID
    db = GetDB()
    searchSession = db.query(SearchSession.id).order_by(desc(SearchSession.id)).first()

    #print("The latest search session is of ID " + str(searchSession.id))
    
    return searchSession.id

def QgetLatestSearchDay():
    db = GetDB()
    searchDay = db.query(SearchDay.id).order_by(desc(SearchDay.id)).first()
    
    return searchDay.id

def InsertSearchSession(date):
    
    db = GetDB()
    
    ss = SearchSession()
    
    ss.searchDate = date
    
    db.add(ss)
    
    db.commit()
    
def InsertSearchDay(day, actualDay):
    
    db = GetDB()
    
    sd = SearchDay()
    
    sd.date = day
    sd.actualDay = actualDay
    
    print(str(day))
   
    #raw_input("day is above")
    
    # This is the save to db bit, that will allow you to try and write but if it exists it wont
    # throw an exception.
    
    db.merge(sd)
    try:
        db.commit() 
        print("Inserted new search day")
    except exc.SQLAlchemyError:
        db.rollback()
        print("found dupes")
        
 
        
    
def GetAllTotalVehiclesBySearchSession(searchSession):
    query = QgetAllSearchVehicles()
    
    for searchVehicle in query:
        
        GetTotalVehicles(searchVehicle.model)   
    
    
    
def GetTotalVehicles(model):
    
    db = GetDB()
        

    count = db.query(AuctionVehicle, SearchVehicle)\
            .join( SearchVehicle.auctionVehicles)\
            .filter(AuctionVehicle.searchSession_id == QgetLatestSearchSession())\
            .filter(SearchVehicle.model==model)\
            .count()
                
       
    latestSess = QgetLatestSearchSession()
        
    print("Searchsession " + str(latestSess) + " has a Total of " + str(count) + " " + " " + GetMake(model) + " " + model + "(S)")
    query = db.query(SearchVehicle)\
                        .filter(SearchVehicle.model == model)\
                        .first()
                        
    # Get current day.
    currentDay = QgetLatestSearchDay()
    
    # Insert the search stats for the current vehicle.                
    InsertSearchStats(latestSess, query.id, count, currentDay)

def SearchStatOps():
    
    
    latestSession = QgetLatestSearchSession()  
    GetAllTotalVehiclesBySearchSession(latestSession)    
    
def DeleteSearchVehicle(searchVehicleId):
    
    db = GetDB()
    
    db.query(VehicleStat).filter(VehicleStat.searchVehicle_id == searchVehicleId).delete()
    
    db.commit()
    
    
    

def InsertSearchStats(searchSession, searchVehicle_id, totalVehicles, day_id):
    
    db = GetDB()
    
    vs = VehicleStat()
    
    vs.searchSession_id = searchSession
    vs.searchVehicle_id = searchVehicle_id
    vs.totalVehicles = totalVehicles
    vs.searchday_id = day_id
    
    
    #this is how to insert stuff but not crash if it finds dupes!
    #there is a compound constraint on this table!
            
    db.merge(vs)
    
    try:
        db.commit()
        print("inserted search stats for vehicle" + str(searchVehicle_id))
    except exc.SQLAlchemyError:
        db.rollback()
        print("found dupes, skipping stats insert.")
        
def InterestedVehicleOps(idList):
    
    # just pass this method a list of lot numbers and should be good to go.
    #idList = [59665,59673,59681,59684]
    
    return GetInterestedVehicles(idList)
        
def GetInterestedVehicles(idList):
    
    vehicleList2 = []
    
    
    for id in idList:
    
        db = GetDB()
                
        result = db.query(AuctionVehicle).filter(AuctionVehicle.id == id).first()
        
        vehicleList2.append(result)
        
            
    for vehicle in vehicleList2:
        print("id is " + str(vehicle.id) + " lotnumber is : " + str(vehicle.lotNumber))
    
    #return the list of selected vehicles
        
    return vehicleList2

def auction_vehicles_latest_search_session():

    session = GetDB()

    search_session_id = QgetLatestSearchSession()

    query = None

    while (query == None):
        query = session.query(AuctionVehicle)\
            .filter(AuctionVehicle.searchSession_id == search_session_id)


        search_session_id -=1
    # If it finds results then break the loop, otherwise decrement the search session until it finds something.
        if (query.count() > 0):
            break

        query = None


    return query

def get_search_vehicles_for_session(ss_id):

    session = GetDB()
    search_vehicles = session.query(SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(AuctionVehicle.searchSession_id == ss_id)

    return search_vehicles

def get_all_auctionvehicles_unviewed():


    db = GetDB()

    query = db.query(AuctionVehicle, SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(or_(AuctionVehicle.beenViewed == False, AuctionVehicle.beenViewed == None))\
    .order_by(desc(SearchVehicle.model))


    return query

def get_all_auction_vehicles_and_search_vehicles_for_session(search_session):

    session = GetDB()

    all_auction_vehicles = session.query(AuctionVehicle, SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(AuctionVehicle.searchSession_id == search_session)

    return all_auction_vehicles

def GetAllFavouritesLastXDays(userId=None, days=None):

    if not userId:
        userId = 2

    #dayId = GetLatestDay()

    db = GetDB()

    today = datetime.now()
    # Round to nearest day
    today = today.replace(hour = 0, minute = 0, second = 0, microsecond = 0)



    #subtract number of days from date
    days_int = int(days)

    search_from_date = today - timedelta(days=int(days_int))

    #get searchday id from date

    id = db.query(SearchDay.id).filter(SearchDay.date >= search_from_date).order_by(SearchDay.id).first()


    query = db.query(AuctionVehicle)\
    .join(Favourite.auctionvehicle)\
    .join(AuctionVehicle.searchVehicle)\
    .filter(and_(Favourite.day_id > id, Favourite.user_id == userId))\
    .order_by(desc(SearchVehicle.model))\
    .all()

    #for item in query:
    #print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
    #print (str(item.id) + " " + str(item.day_id))


    return query

#GetAllFavouritesByModel('HIACE VAN')


#GetAllFavouritesToday()
        
#InsertFavourite(GetLatestDay(), 49489, 2)

#InterestedVehicleOps()
        
#DeleteSearchVehicle(57)
        
#PrintSearchSessionTotals()
    
#PrintSearchSessionTotals()       
#PrintDayTotalResults()       
    
#QgetTotalVehiclesToday("TOYOACE")    
    
#ayTotal_Insert("HIACE VAN")       
#DayTotal_Update(3, 10, 20)



#SearchStatOps()   
    

#Begin()


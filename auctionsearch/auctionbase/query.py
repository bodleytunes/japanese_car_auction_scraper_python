'''
Created on 22 Nov 2011

@author: jon
'''
import sys




from model import *
from datetime import *

from sqlalchemy import *
from sqlalchemy import create_engine    
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct


from auctionsearch.main import start
sys.path.append("c:\AuctionScraper\MyWeb\src\webstuff")
import emailer


mongoConn = None




def Begin():
    
    collection = GetMongoDb()
    GetAllMongoVehicles(collection)
    
def initalMongoOps():
    collection = GetMongoDb()
    mongoCursor = GetAllMongoVehicles(collection)
    
    return mongoCursor
 
        
    
def GetMongoDb():
    
    global mongoConn
    
    mongoConn = start.ConnectMongo()
    mongodb = start.GetDb(mongoConn)
    collection = start.GetMongoWebPageCollection(mongodb)
    
    return collection

def CloseMongoDb():
    mongoConn.disconnect()


def GetAllMongoVehicles(collection):
    
    cursor = collection.find({"postgresExport" : False})
      
    return cursor
    
     

def GetDB():
    db = alchemysession
    
    return db
    
def QgetAllVehicles():
    
    db = GetDB()
    
    query = db.query(AuctionVehicle).all()
    
    #print(query)
    #print(query[0].lotNumber)
    
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
        
def TranslationGetAll():
    
    db = GetDB()
    
    
    vehicles = db.query(AuctionVehicle)\
                .filter(AuctionVehicle.flagTranslation == True)\
                .order_by(desc(AuctionVehicle.searchSession_id))
    
    return vehicles
                

        
def TranslateOps(vehiclesForTranslation, user_id):
    
    
    
    for vehicle in vehiclesForTranslation:
       
        FlagForTranslation(vehicle)

def InsertFavourite(latestDay, auctionVehicleId, userId):
    
    db = GetDB()
    
    fave = Favourite()
    fave.auctionvehicle_id = auctionVehicleId
    fave.day_id = latestDay
    fave.user_id = userId
    
    db.merge(fave)
    try:
        db.commit() 
        #print("Inserted new favourite")
    except exc.SQLAlchemyError:
        db.rollback()
        #print("found dupes")
        
def FlagForTranslation(vehicle_id):
    
    db = GetDB()
    
    db.query(AuctionVehicle)\
    .filter(AuctionVehicle.id == vehicle_id)\
    .update({AuctionVehicle.flagTranslation : True})
    
    try:
        db.commit() 
        print("Flagged for translation")
    except exc.SQLAlchemyError:
        db.rollback()
        print("Already Flagged.")
    
        
def GetAllUsers():
    
    db = GetDB()
    
    users = db.query(User).all()
    
    return users

def GetAllAuctionvehiclesToday(userId=None, dayId=None):
    
    if not userId:
        userId = 2
    if not dayId:
        dayId = GetLatestDay()
    
    db = GetDB()
    
    query = db.query(AuctionVehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(and_(AuctionVehicle.day_id == dayId, AuctionVehicle.year < 2005))\
            .order_by(desc(SearchVehicle.model))\
            .all()
            
   
    return query

def get_all_auctionvehicles_unviewed():



    db = GetDB()

    query = db.query(AuctionVehicle, SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(or_(AuctionVehicle.beenViewed == False, AuctionVehicle.beenViewed == None))\
    .order_by(desc(SearchVehicle.model))\



    return query

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
            .order_by(desc(SearchVehicle.model))\
            .all()
            
    for item in query:
        print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
        #print (str(item.id) + " " + str(item.day_id))    
        
 
    return query


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
    search_from_date = today - timedelta(days=days_int)

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

def mark_selected_as_viewed(cursor=None):


    #cursor = get_all_auction_vehicles_for_session(558)

    #auction_vehicles = cursor.all()
    session = GetDB()

   ## db.query(AuctionVehicle)\
   ## .filter(AuctionVehicle.id == vehicle_id)\
   ## .update({AuctionVehicle.flagTranslation : True})

    for vehicle in cursor:
        session.query(AuctionVehicle)\
                .filter(AuctionVehicle.id == vehicle.id)\
                .update({AuctionVehicle.beenViewed : True})

    #test_cursor.update({AuctionVeYou are in ahicle.flagToSendEmail : True})

    try:
        session.commit()
    #print("Flagged for translation")
    except exc.SQLAlchemyError:
        session.rollback()
    #print("Already Flagged.")









def GetAllFavouritesAll(userId=None, dayId=None):
    
    if not userId:
        userId = 2
#    if not dayId:
#        dayId = GetLatestDay()
    
    db = GetDB()
    
    query = db.query(AuctionVehicle)\
            .join(Favourite.auctionvehicle)\
            .join(AuctionVehicle.searchVehicle)\
            .filter(Favourite.user_id == userId)\
            .order_by(desc(Favourite.day_id))\
            .all()
            
    for item in query:
        print (str(item.lotNumber) + " " + str(item.year) + " " + item.searchVehicle.make + " " + item.searchVehicle.model)
        #print (str(item.id) + " " + str(item.day_id))    
        
 
    return query

def GetAllFavouritesCounts():
    
    db = GetDB()
    
    queryCount = db.query(func.count(Favourite.auctionvehicle_id))\
            .join(Favourite.auctionvehicle)\
            .join(Favourite.day)\
            .order_by(Favourite.day_id)\
            .group_by(Favourite.day_id)
            
    # Convert to normal list of integers
    newCount = [int(e[0]) for e in queryCount]
            
    return newCount



def GetAllFavouritesGroupByDay():
    
    db = GetDB()
        
    query = db.query(Favourite)\
            .join(Favourite.auctionvehicle)\
            .join(Favourite.day)\
            .distinct(Favourite.day_id)\
            .order_by(Favourite.day_id)\
            .all()
            
    return query
            
                
#    i = 0
            
            
#    for item in query:
#        #print(item.auctionvehicle.id)
#        print(item.day.actualDay + " " + str(item.day.date))
#        total = str(queryCount[i])
#        print("Total favourites: " + str(total))
#        i = i + 1
        
        
        
    
        
        
      
    
             
        
        
    #average = session.query(func.avg(sums.subquery().columns.a1)).scalar()
                    
#    favesdays = db.query(SearchDay)\
#                    .filter(SearchDay.id.in(favedays_subq))\
#                    .all()
#                    
#    print(favedays)                 
   
                  
    
#    address_subq = session.query(Address).\
#                    filter(Address.email_address == 'ed@foo.com').\
#                    subquery()
#
#    q = session.query(User).join(address_subq, User.addresses)

#from sqlalchemy import func
#
## count User records, without
## using a subquery.
#session.query(func.count(User.id))
#            
## return count of user "id" grouped
## by "name"
#session.query(func.count(User.id)).\
#        group_by(User.name)
#
#from sqlalchemy import distinct
#
## count distinct "name" values
#session.query(func.count(distinct(User.name)))
                 


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
                  remoteurlfin=None,\
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
    avehicle.remoteurlfin = remoteurlfin
    #Set the search session foreign key
    avehicle.searchSession_id = searchSession
    avehicle.day_id = dayId
    avehicle.beenViewed = False
    try:
        avehicle.searchVehicle_id = get_model_id(make, model)
    except:
        InsertSearchVehicle(make, model)
        avehicle.searchVehicle_id = get_model_id(make, model)
    
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

def GetAllVehiclesReturnsIds():
    db = GetDB()
    
    
    
    query = db.query(SearchVehicle.id).all()
    
    
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
    
    
    
    latest_search_day = db.query(SearchDay).order_by(desc(SearchDay.id)).first()
    
    if(latest_search_day.date != day):
        
    
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
        
    #print("Searchsession " + str(latestSess) + " has a Total of " + str(count) + " " + " " + GetMake(model) + " " + model + "(S)")
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
    
def DeleteAuctionVehicle(AuctionVehicleId):
    
    db = GetDB()
    
    db.query(AuctionVehicle).filter(AuctionVehicle.id == AuctionVehicleId).delete()
    
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

def get_model_from_id(searchVehicle):
    # give it a model id and return the model string.
    db = GetDB()
    
    model = db.query(SearchVehicle.model).filter(SearchVehicle.id == searchVehicle).first()
    
    return model

def test():

    model = get_model_from_id(57)
    
    raw_input(model)
    
    if model == "SAMBAR" or model == "DOMINGO":
        print "sc-vanning@googlegroups.com"
    
    elif model == "HIACE VAN":
        print "supercamper@googlegroups.com"
    
    elif model == "ASTRO" or \
                    model == "CHEVROLET ASTRO":
        
        print "sc-astro@googlegroups.com"
    
    elif model == "CHEVROLET CHEVY VAN" or \
                    model == "CHEVY VAN" or \
                    model == "DODGE DODGE RAM" or \
                    model == "DODGE RAM" or \
                    model == "RAM" or \
                    model == "ECONOLINE" or \
                    model == "FORD ECONOLINE":
        
        print "sc-g20@googlegroups.com"
    
    else:
        
        print "supercamper.auctions@gmail.com"

    
    

def CustomAlertRoutine():
    
    # Check for Classic Dodge Ram
    CustomCheck_classic_dodge_ram()
   
        
    

def CustomCheck_classic_dodge_ram():
    
    max_year = 1993
    model = "DODGE RAM"
    # for testing
    #latestSearchSession = 50
    latestSearchSession = None
    
    
    if latestSearchSession is None:
        
        #Get latest search session ID
        latestSearchSession = QgetLatestSearchSession()
    
    db = GetDB()
    
    count = db.query(AuctionVehicle, SearchVehicle)\
                .join(SearchVehicle.auctionVehicles)\
                .filter(and_(AuctionVehicle.year < max_year,\
                        SearchVehicle.model == model, \
                        AuctionVehicle.searchSession_id == latestSearchSession))\
                .count()
    
   
                    
    
    print "The number of special vehicles return is " + str(count)
                
    if (count > 0):
        vehicles = db.query(AuctionVehicle, SearchVehicle)\
                .join(SearchVehicle.auctionVehicles)\
                .filter(and_(AuctionVehicle.year < max_year,\
                        SearchVehicle.model == model, \
                        AuctionVehicle.searchSession_id == latestSearchSession))\
                        .all()
    
        # Send special alert email with details of the vehicle found
        print ("FOUND SPECIAL VEHICLE (dodge ram) - EMAILING THE RESULTS")
        emailer.special_alert_email(vehicles, "CLASSIC DODGE RAM", int(count))
        
def select_test_query():
    db = GetDB()
    
    vehicles = db.query(AuctionVehicle).filter(or_(AuctionVehicle.imgurl1 == "http://1.ajes.com/imgs/4IuzCwB6Lua4jzKEDpTRXZOJDqxPBttFSc4OQ2ixKQxK9c92i1v1A2WCy3RKisYlQPb7Ban3Lu-UBBc5vZmDZ8XLz", AuctionVehicle.imgurl2 == "http://1.ajes.com/imgs/4IuzCwB6Lua4jzKEDpTRXZOJDqxPBttFSc4OQ2ixKQxK9c92i1v1A2WCy3RKisYlQPb7Ban3Lu-UBBc5vZmDZ8XLz", AuctionVehicle.imgurl3 == "http://1.ajes.com/imgs/4IuzCwB6Lua4jzKEDpTRXZOJDqxPBttFSc4OQ2ixKQxK9c92i1v1A2WCy3RKisYlQPb7Ban3Lu-UBBc5vZmDZ8XLz")).all()
    
    for item in vehicles:
        print str(item.year) + " " + item.imgurl1
        
def select_test_query_2(search_vehicle_id):
    db = GetDB()
    
    vehicles = db.query(AuctionVehicle)\
                .join(AuctionVehicle.searchVehicle)\
                .filter(SearchVehicle.id == search_vehicle_id).all()
    
    for item in vehicles:
        DeleteAuctionVehicle(item.id)
      
    
    for item in vehicles:
        print (str(item.id))

def get_search_vehicles_for_session(ss_id):

    session = GetDB()
    search_vehicles = session.query(SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(AuctionVehicle.searchSession_id == ss_id)\
    .distinct()

    return search_vehicles

def get_auction_vehicles_for_session(search_session, search_vehicle):

    session = GetDB()

    auction_vehicles = session.query(AuctionVehicle)\
            .join(SearchVehicle.auctionVehicles)\
            .filter(and_(SearchVehicle.id == search_vehicle, AuctionVehicle.searchSession_id == search_session))


    return auction_vehicles

def get_all_auction_vehicles_for_session(search_session):

    session = GetDB()

    all_auction_vehicles = session.query(AuctionVehicle)\
                    .filter(AuctionVehicle.searchSession_id == search_session)

    return all_auction_vehicles

def get_all_auction_vehicles_and_search_vehicles_for_session(search_session):

    session = GetDB()

    all_auction_vehicles = session.query(AuctionVehicle, SearchVehicle)\
    .join(SearchVehicle.auctionVehicles)\
    .filter(AuctionVehicle.searchSession_id == search_session)

    return all_auction_vehicles



def get_search_sessions_by_date(floor_date):

    session = GetDB()

    search_sessions = session.query(SearchSession)\
                    .filter(SearchSession.searchDate > floor_date)

    return search_sessions


#session = GetDB()
#vehicles = session.query(AuctionVehicle.id).filter(and_(AuctionVehicle.id > 1, AuctionVehicle.id < 126700))

#mark_selected_as_viewed(vehicles)


#mark_selected_as_viewed()



#sv = get_search_vehicles_for_session(466)

#for item in sv.all():
    #print item.id

    
    

#select_test_query_2(81)

#test()
       
        
#CustomCheck_classic_dodge_ram()
#GetAllFavouritesByDay()

# This fixed the problems!
#GetAllFavouritesByModel('HIACE VAN')


#GetAllFavouritesToday()
        
#InsertFavourite(GetLatestDay(), 49489, 2)

#InterestedVehicleOps()
        
#DeleteSearchVehicle(57)
        

    
#PrintSearchSessionTotals()       
#PrintDayTotalResults()     
#GetAllVehiclesReturnsIds()  
    
#QgetTotalVehiclesToday("TOYOACE")    
    
#ayTotal_Insert("HIACE VAN")       
#DayTotal_Update(3, 10, 20)



#SearchStatOps()   
    

#Begin()

#db = GetDB()



    
    



    

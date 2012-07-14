'''
Created on 11 Feb 2012

@author: jonny boy clayton
'''
#from flask import url_for

from jinja2 import Template, Environment, PackageLoader
from auctionsearch.auctionbase import model



from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from datetime import *
from datetime import timedelta
from datetime import date
from mailer import *

smtp_mail_server = "mailex"

extra_alert_destination_address = "supercamper.uk@gmail.com"

def special_alert_email(vehicles, vehicleModel, count):
    
    global smtp_mail_server
    global extra_alert_destination_address
             
    # Render template to string with Jinja2
    
    env = Environment(loader=PackageLoader('emailer', 'templates'))
   
    #t = env.get_template('vehicle_for_render.html')
    t = env.get_template('email_initial_view_lite.html')
    html = t.render(vehicles=vehicles, count=count)
    #htmlEncoded = html.encode('utf8')
    #print html
    
    
    ## EMAIL STUFF ###         
    message = Message()
    message.From = "supercamper.uk@gmail.com"
    message.To = extra_alert_destination_address
    message.Subject = "[SC Auto SPECIAL ALERT EMAIL!] " + "## " + unicode(vehicleModel) + " ## " 
    #message.Body = messageBody
    message.Html = html
    mailer = Mailer(smtp_mail_server)
    mailer.send(message)

def send_html_email(searchVehicle):
    
    global smtp_mail_server
   
    
    newDay = datetime.now()
    #   # trim todays date
    date = newDay.replace(hour=0,minute=0,second=0,microsecond=0)
    
    #Number of historical days of vehicles to get.
    numberOfDays = 1
    
    date = date - timedelta(days=int(numberOfDays))
    
    from auctionsearch.auctionbase import query
    
    db = query.GetDB()
    
    searchSession = query.QgetLatestSearchSession()

    string_model = db.query(model.SearchVehicle.id).filter(model.SearchVehicle.id == searchVehicle).first()

    if string_model == "SAMBAR":
        raw_input ("about to do SUBARU SAMBARS!")


# Check type of vehicle to see if should span all years.

    if (string_model[0] == "CAMROAD"):

        cursor = query_all_years(searchVehicle, searchSession, date)
        count = query_all_years_count(searchVehicle, searchSession, date)
    else:
        cursor = query_sub_2002(searchVehicle, searchSession, date)
        count = query_sub_2002_count(searchVehicle, searchSession, date)


    modelName = db.query(model.SearchVehicle.model).filter(model.SearchVehicle.id == searchVehicle).first()
    #raw_input("model name just retrieved is " + str(modelName))
    if modelName == "SAMBAR":

        raw_input("about to EMAIL SAMBARS!")


    if count > 0:

        if modelName == "SAMBAR":
            raw_input("now in the emailer function about to email sambars")

        destinationAddress = None 
        # Get the destination email address
        destinationAddress = check_vehicle_type(modelName[0])

        if modelName == "SAMBAR":
            raw_input("destination address is" + destinationAddress )

        # Render template to string with Jinja2
        
        env = Environment(loader=PackageLoader('emailer', 'templates'))
       
        #t = env.get_template('vehicle_for_render.html')
        t = env.get_template('email_initial_view_lite.html')
        html = t.render(vehicles=cursor, count=count)
        #htmlEncoded = html.encode('utf8')
        #print html
        #raw_input("Destination addresss is " + destinationAddress)
        
        ## EMAIL STUFF ###         
        message = Message()
        message.From = "supercamper.uk@gmail.com"
        message.To = destinationAddress
        message.Subject = "[SC Auto Search] " + "## " + unicode(modelName) + " ## "  + str(count) + " " + "Vehicles" 
        #message.Body = messageBody
        message.Html = html
        mailer = Mailer(smtp_mail_server)
        mailer.send(message)
            
def check_vehicle_type(modelName):
        
        #from auctionsearch.auctionbase import query
        
        #model = query.get_model_from_id(searchVehicle)
        
        # This is where it chooses which mailing list to send to #
    
        if modelName == "SAMBAR" or modelName == "DOMINGO":
            
            print "funky vanning vans"
            return "sc-vanning@googlegroups.com"
        
        if modelName == "BONGO FRIENDEE":
            
            #print "funky vanning vans"
            return "sc-bongo@googlegroups.com"
        
        
        elif modelName == "HILUX" or \
                    modelName == "RODEO" or \
                    modelName == "FARGO" or \
                    modelName == "FARGO TRUCK" or \
                    modelName == "DELICA" or \
                    modelName == "DELICA TRUCK":
                    
            print "COACH BUILT"
            return "sc-delica@googlegroups.com"
        
        elif modelName == "CAMROAD" or \
             modelName == "TOYOACE" or \
             modelName == "DYNA":
        
            return "sc-dyna@googlegroups.com"
        
        elif modelName == "TOWNACE TRUCK" or \
             modelName == "LITEACE TRUCK" or \
              modelName == "LITE ACE TRUCK" or \
               modelName == "TOWN ACE TRUCK":
        
        
            return "sc-townace@googlegroups.com"
        
        elif modelName == "ELF TRUCK" or \
                    modelName == "ELF":
            
            return "sc-elf@googlegroups.com"
        
        elif modelName == "ASTRO" or \
                        modelName == "CHEVROLET ASTRO" or \
                        modelName == "SAFARI" or \
                        modelName == "GMC SAFARI" or \
                        modelName == "GM CHEVROLET" or \
                        modelName == "CHEVROLET CHEVROLET ASTRO" or \
                        modelName == "GM ASTRO" or \
                        modelName == "GM SAFARI":
            print "small american day van"
            return "sc-astro@googlegroups.com"
        
        elif modelName == "CHEVROLET CHEVY VAN" or \
                        modelName == "CHEVY VAN" or \
                        modelName == "VANDURA" or \
                        modelName == "GM VANDURA" or \
                        modelName == "GMC VANDURA":
            print "large american g20 type day van"
            return "sc-g20@googlegroups.com"
        
        elif modelName == "ECONOLINE" or \
                        modelName == "FORD ECONOLINE" or \
                        modelName == "GM EXPRESS" or \
                        modelName == "GMC EXPRESS" or \
                        modelName == "EXPRESS":
            print "large american ford based day van or camper"
            return "sc-express@googlegroups.com"
        # DODGE RAM GO HERE
        elif modelName == "DODGE DODGE RAM" or \
                        modelName == "DODGE RAM" or \
                        modelName == "RAM":
            print "large american day van based on dodge ram"
            return "sc-dodge-ram@googlegroups.com"
        # Sporty models go here
        elif modelName ==   "ARISTO" or \
                        modelName == "TOYOTA ARISTO" or \
                        modelName == "RX-7" or \
                        modelName == "RX7":
            print "sports cars and toyota aristo"
            return "sc-aristo@googlegroups.com"
        # HIACE GO HERE
        elif modelName == "HIACE" or \
             modelName == "HIACE VAN" or \
             modelName == "HIACE TRUCK":
                       
            print "Hiace type vans"
            return "sc-hiace@googlegroups.com"

        else:
            
            return "supercamper@googlegroups.com"

def query_sub_2002(searchVehicle, searchSession, date):
    
    from auctionsearch.auctionbase import query
    
    db = query.GetDB()
    
    cursor = db.query(model.AuctionVehicle)\
    .join(model.AuctionVehicle.searchDay)\
    .join(model.AuctionVehicle.searchVehicle)\
    .filter(and_(model.SearchVehicle.id == searchVehicle, model.SearchDay.date >= date, model.AuctionVehicle.searchSession_id == searchSession, model.AuctionVehicle.year < 2002))\
    .order_by(desc(model.SearchDay.date))\
    .all()

    return cursor

def query_sub_2002_count(searchVehicle, searchSession, date):
    from auctionsearch.auctionbase import query
    
    db = query.GetDB()
    
    count = db.query(model.AuctionVehicle)\
    .join(model.AuctionVehicle.searchDay)\
    .join(model.AuctionVehicle.searchVehicle)\
    .filter(and_(model.SearchVehicle.id == searchVehicle, model.SearchDay.date >= date, model.AuctionVehicle.searchSession_id == searchSession, model.AuctionVehicle.year < 2002))\
    .order_by(desc(model.SearchDay.date))\
    .count()

    return count

def query_all_years(searchVehicle, searchSession, date):
    from auctionsearch.auctionbase import query
    db = query.GetDB()
    
    cursor = db.query(model.AuctionVehicle)\
    .join(model.AuctionVehicle.searchDay)\
    .join(model.AuctionVehicle.searchVehicle)\
    .filter(and_(model.SearchVehicle.id == searchVehicle, model.SearchDay.date >= date, model.AuctionVehicle.searchSession_id == searchSession))\
    .order_by(desc(model.SearchDay.date))\
    .all()

    return cursor


def query_all_years_count(searchVehicle, searchSession, date):
    from auctionsearch.auctionbase import query
    db = query.GetDB()
    
    count = db.query(model.AuctionVehicle)\
    .join(model.AuctionVehicle.searchDay)\
    .join(model.AuctionVehicle.searchVehicle)\
    .filter(and_(model.SearchVehicle.id == searchVehicle, model.SearchDay.date >= date, model.AuctionVehicle.searchSession_id == searchSession))\
    .order_by(desc(model.SearchDay.date))\
    .count()

    return count





        
            
            
                

        
    
            

    


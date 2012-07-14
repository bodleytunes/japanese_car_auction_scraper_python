'''
Created on 6 Nov 2011

@author: jon
'''
from mongoengine import *
from WebPage import *


def begin():
    inputdata = ""
    inputdata = raw_input("Do you want to add a vehicle?")
    if inputdata == "y" or inputdata == "Y":
            print("playing get input")
            GetInput()
            begin()
            
    elif inputdata == "n":
        exit
    else:
        begin()
        
   
        
   

def GetInput():
    connect("Auctionvehicles",host="jmcmongo")
    
    searchVehicle = MongoSearchVehicle()
    make = getMake()
   
    
    model = getModel()
    
    searchVehicle.make = make
    searchVehicle.model = model
    try:
        searchVehicle.save()
        print("Saved to DB...")
    except:
        print "duplicate - not saved"
        pass
    
   
    
def getModel():
    model = raw_input("Enter Model: ")
    
    if model == "":
        print("enter something please")
        getModel()
        
    return model
        
    
        
def getMake():
    make = raw_input("Enter Make: ")
    
    if make == "":
        print("enter something please")
        getMake()
        
    return make
    
        
    

begin()


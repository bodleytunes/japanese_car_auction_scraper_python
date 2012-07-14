'''
Created on 5 Nov 2011

@author: jon
'''

from mongoengine import *


class WebPage():
    '''
    classdocs
    '''


    def __init__(self,Make=None,Model=None,imgUrl1=None,imgUrl2=None,imgUrl3=None,remoteUrl=None,lotNumber=None,year=None,cc=None,mileage=None,price=None,chassis=None,auctionHouse=None,superCamperNumber=None,postgresExport=None):
        '''
        Constructor
        '''
        self.make = Make
        self.model = Model
        self.imgurl1 = imgUrl1
        self.imgurl2 = imgUrl2
        self.imgurl3 = imgUrl3
        self.remoteUrl = remoteUrl
        self.lotnumber = lotNumber
        self.year = year
        self.cc = cc
        self.mileage = mileage
        self.price = price
        self.chassis = chassis
        self.auctionHouse = auctionHouse
        self.superCamperNumber = superCamperNumber
        self.postgresExport = postgresExport
        
        
class SearchVehicle():
    
    def __init__(self,make=None,model=None):
        
        self.make=make
        self.model=model
        
class MongoSearchVehicle(Document):
            
    make=StringField()
    model=StringField(unique=True)
    
        
        
class MongoWebPage(Document):
    
    make = StringField()
    model = StringField()
    
    imgurl1 = URLField(max_length=400, required=False, unique=True)
    imgurl2 = URLField(max_length=400, required=False)
    imgurl3 = URLField(max_length=400, required=False)
    remoteUrl = URLField(max_length=255, required=False)
    lotnumber = StringField(max_length=10, required=False)
    year = StringField(max_length=8, required=False)
    cc = StringField(max_length=8, required=False)
    mileage = StringField(max_length=8, required=False)
    price = StringField(max_length=20, required=False)
    chassis = StringField(max_length=30, required=False)
    auctionHouse = StringField(max_length=40, required=False)
    superCamperNumber = StringField(max_length=10, required=False)
    dateAdded = DateTimeField()
    postgresExport = BooleanField(required=False)
    

class MongoUser(Document):
            
    userName=StringField()
    email=StringField(unique=True)
    
class UserVehicleFavorite(Document):
    favoriteDate=DateTimeField()
    # Important, this allows for a compound unique index
    # can't have the same two fields using unique field with
    userId=ObjectIdField(unique_with="vehicleId")
    vehicleId=ObjectIdField()
    
    
    
    

    
    
    
    
    
        

    
    
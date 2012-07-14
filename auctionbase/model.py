'''
Created on 14 Nov 2011

@author: jon
'''

#from elixir import *
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# an Engine, which the Session will use for connection
# resources
new_engine = create_engine('postgresql://postgres:postgres@jmcmongo:5432/test')

# create a configured "Session" class
NewSession = sessionmaker(bind=new_engine)

# create a Session
alchemysession = NewSession()


class SearchVehicle(Base):
    # This is the actual table name in the database...
    __tablename__ = 'model_searchvehicle'
    id = Column(Integer, primary_key=True)
    make = Column(String, nullable=True)
    model = Column(String, nullable=True)
    descriptive = Column(String, nullable=True)
    auctionVehicles = relationship("AuctionVehicle", backref="model_searchvehicle")
    vehicleStats = relationship("VehicleStat", backref="model_searchvehicle")
    
    vehicleType_id = Column(Integer, ForeignKey('model_vehicletype.id'))
    vehicleType = relationship("VehicleType", backref='model_searchvehicle')
    
    vehicleTypeSize_id = Column(Integer, ForeignKey('model_vehicletypesize.id'))
    vehicleTypeSize = relationship("VehicleTypeSize", backref='model_searchvehicle')
    
    vehicleCountry_id = Column(Integer, ForeignKey('model_vehiclecountry.id'))
    vehicleCountry = relationship("VehicleCountry", backref='model_searchvehicle')

class Customer(Base):
    __tablename__ = 'model_customer'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=True)
    emailAddress = Column(String, nullable=True)

class Customer2searchVehicle(Base):
    __tablename__ = 'model_customer2searchvehicle'
    id = Column(Integer, primary_key=True)
    
    customer_id = Column(Integer, ForeignKey('model_customer.id'))
    customer = relationship("Customer", backref='model_customer2searchvehicle')
    
    searchvehicle_id = Column(Integer, ForeignKey('model_searchvehicle.id'))
    searchvehicle = relationship("SearchVehicle", backref='model_customer2searchvehicle')
  
class Day2SearchVehicle(Base):
    __tablename__ = 'model_day2searchvehicle'
    
    id = Column(Integer, primary_key=True)
    
    day_id = Column(Integer, ForeignKey('model_searchday.id'))
    day = relationship("SearchDay", backref='model_day2searchvehicle')
    
    searchvehicle_id = Column(Integer, ForeignKey('model_searchvehicle.id'))
    searchvehicle = relationship("SearchVehicle", backref='model_day2searchvehicle')
    
    totalvehicles = Column(Integer, nullable=True)
    
class Favourite(Base):
    
    __tablename__ = 'favourite'
    id = Column(Integer, primary_key=True)
    
    day_id = Column(Integer, ForeignKey('model_searchday.id'))
    day = relationship("SearchDay", backref='favourite')
    
    auctionvehicle_id = Column(Integer, ForeignKey('model_auctionvehicle.id'))
    auctionvehicle = relationship("AuctionVehicle", backref='favourite')
    
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship("User", backref='favourite')
    
class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    username = Column(String, nullable=True)
    email = Column(String, nullable=True)
     
    
class VehicleType(Base):
    __tablename__ = 'model_vehicletype'
    id = Column(Integer, primary_key=True)
    type = Column(String,nullable=True)
    searchVehicles = relationship("SearchVehicle", backref="VehicleType")
    
class VehicleTypeSize(Base):
    __tablename__ = 'model_vehicletypesize'
    id = Column(Integer, primary_key=True)
    typeSize = Column(String,nullable=True)
    searchVehicles = relationship("SearchVehicle", backref="VehicleTypeSize")
    
class VehicleCountry(Base):
    __tablename__ = 'model_vehiclecountry'
    id = Column(Integer, primary_key=True)
    country = Column(String,nullable=True)
    searchVehicles = relationship("SearchVehicle", backref="VehicleCountry")
    
    
class SearchSession(Base):
    __tablename__ = 'model_searchsession'
    id = Column(Integer, primary_key=True)
    searchDate = Column(DateTime, nullable=True)
    auctionVehicles = relationship("AuctionVehicle", backref="model_searchsession")
    searchStats = relationship("VehicleStat", backref="model_searchsession")
    
class SearchDay(Base):
    __tablename__ = 'model_searchday'
    id = Column(Integer, primary_key=True)
    date = Column(DateTime, nullable=True)
    actualDay = Column(String, nullable=True)
    

class VehicleStat(Base):
    __tablename__ = 'model_vehiclestats'
    id = Column(Integer, primary_key=True)
    
    searchVehicle_id = Column(ForeignKey("model_searchvehicle.id"), nullable=True)
    SearchVehicle = relationship("SearchVehicle", backref="model_vehiclestats")
    
    searchSession_id = Column(ForeignKey("model_searchsession.id"), nullable=True)
    
    
    totalVehicles = Column(Integer, nullable=True)
    
    SearchDay = relationship("SearchDay", backref="model_vehiclestats")
    searchday_id = Column(ForeignKey("model_searchday.id"), nullable=True)
    
    
    
    

class AuctionVehicle(Base):
    # Actual DB table name goes here->...
    __tablename__ = 'model_auctionvehicle'
    
    id = Column(Integer, primary_key=True)
    searchVehicle_id = Column(Integer, ForeignKey('model_searchvehicle.id'))
    searchVehicle = relationship("SearchVehicle", backref='model_auctionvehicle')
    searchSession_id = Column(Integer, ForeignKey('model_searchsession.id'))
    searchSession = relationship("SearchSession", backref='model_auctionvehicle')
    day_id = Column(Integer, ForeignKey('model_searchday.id'))
    searchDay = relationship("SearchDay", backref='model.auctionvehicle')
    
    lotNumber = Column(Integer, nullable=True)
    auctionHouse = Column(String, nullable=True)
    miles = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    chassis = Column(String, nullable=True)
    imgurl1 = Column(String, nullable=True)
    imgurl2 = Column(String, nullable=True)
    imgurl3 = Column(String, nullable=True)
    remoteurl = Column(String, nullable=True)
    flagToSendEmail = Column(Boolean, nullable=True)

    

    
  
   
    

    
    
    
    
    

    
    
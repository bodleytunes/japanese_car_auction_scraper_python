'''
Created on 13 Nov 2011

@author: jon
'''
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.orm import mapper
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from elixir import *


Base = declarative_base()

def Begin():
    
    db = create_engine('postgresql://postgres:postgres@jmcmongo:5432/test')
    
    metadata.bind = "postgresql://postgres:postgres@jmcmongo:5432/test"
    metadata.bind.echo = True
    

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    fullname = Column(String)
    password = Column(String)
   
Begin()

    
    
    
    
    

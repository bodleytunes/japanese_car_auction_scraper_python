'''
Created on 7 Nov 2011

@author: jon
'''

'''
Created on 6 Nov 2011

@author: jon
'''
from mongoengine import *
from WebPage import *


def begin():
    inputdata = ""
    inputdata = raw_input("Do you want to add a user?")
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
    
    mongoUser = MongoUser()
    name = getName()
   
    
    email = getEmail()
    
    mongoUser.userName = name
    mongoUser.email = email
    try:
        mongoUser.save()
        print("Saved to DB...")
    except:
        print "duplicate - not saved"
        pass
    
   
    
def getName():
    name = raw_input("Enter name: ")
    
    if name == "":
        print("enter something please")
        getName()
        
    return name
        
    
        
def getEmail():
    email = raw_input("Enter email: ")
    
    if email == "":
        print("enter something please")
        getEmail()
        
    return email

class MongoUser(Document):
            
    userName=StringField()
    email=StringField(unique=True)
    


    
        
    

begin()





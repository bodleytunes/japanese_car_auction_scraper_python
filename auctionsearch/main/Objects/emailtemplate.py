'''
Created on 9 Nov 2011

@author: jon
'''

class EmailTemplate(object):
    '''
    classdocs
    '''


    def __init__(self,userId=None,userEmail=None,vehicleWebpageId=None,vehicleMake=None,vehicleModel=None,totalVehicles=None):
        '''
        Constructor
        '''
        self.userId = userId
        self.userEmail = userEmail
        self.vehicleWebpageId = vehicleWebpageId
        self.vehicleMake = vehicleMake
        self.vehicleModel = vehicleModel
        self.totalVehicles = totalVehicles
        
        
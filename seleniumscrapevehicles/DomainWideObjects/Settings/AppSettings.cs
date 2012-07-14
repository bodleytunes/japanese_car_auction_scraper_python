using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;

namespace DomainWideObjects.Settings {
    public static class AppSettings
    {
        // single search settings
        public static string singleSearchVehicleMake = "FORD";
        public static string singleSearchVehicleModel = "FORD ECONOLINE";
    

        // Single search mode on / off ?
        public static bool manualSingleSearchMode = false;
        
        // Global search get current search make and model.
        public static string globalMake;
        public static string globalModel;

     

        public static void setCurrentVehicle(int vehicleID) {
              
        
            //Get vehicle make / model

            var context = new seleniumScrapeEntities();
                   
            globalMake = (from v in context.tblVehicles
                            where v.Vehicle_ID_Pk == vehicleID
                            select v.Vehicle_Make).First();

            globalModel = (from db in context.tblVehicles
                           where db.Vehicle_ID_Pk == vehicleID
                           select db.Vehicle_Model).First();

            //var makeList = makeQuery.ToList();



            // IQueryable<string> modelQuery = from db in context.tblVehicles
            //                where db.Vehicle_ID_Pk == vehicleID
            //              select db.Vehicle_Model;



            //var modelList = modelQuery.ToList();



            //   var vehicleData = new Vehicle()
            //                        {
            //                            vehicleMake = makeList[0],
            //                            vehicleModel = modelList[0]
            //                       };




        }
        
    }
}

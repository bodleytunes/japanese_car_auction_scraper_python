using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Repository;
using DomainWideObjects.Settings;

namespace SeleniumTestMain.General {
    public class SearchTypeChooser : ISearchTypeChooser
    {


        public List<tblVehicle> ChooseTypeOfSearch(List<tblVehicle> vehicleSearchList) {
           
            // create instance of dbreader class to read vehicles to search.
            if (!AppSettings.manualSingleSearchMode) {
                // Multiple search
                var dbReader = new DBreader();
                vehicleSearchList = dbReader.readSearchVehicles();
                
            } else {
                //Single Search
                var dbReader = new DBreader();
                vehicleSearchList = dbReader.GetSingleSearchVehicle(AppSettings.singleSearchVehicleModel);

               
            }

            return vehicleSearchList;
        }
    }
}

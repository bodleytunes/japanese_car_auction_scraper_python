using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects;
using SeleniumTestMain.General;
using SeleniumTestMain.General.Data;

namespace SeleniumTestMain {
    public class Main
    {
        private string tableHTMLtagToScrape = "t_main";
        

        public void MainMethod()
        {
            Navigator navigator = new Navigator();
           // Instanciate objects in the navigator
            navigator.Create();
            // navigate to page
            navigator.NavigateToPage();
            // login to page - return the selenium driver into the var.
            var driver = navigator.LoginToPage();
            // Select Make
            IVehicleSelector vehicleSelector = new VehicleSelector(driver);
            vehicleSelector.SelectMake();
            
            // Select Model
            vehicleSelector.SelectModel();
            // Condition Picker
            var conditionPicker = new ConditionPicker(driver);
          
            // Click condition list
            conditionPicker.ClickConditions();

            // Check for the number of pages of the vehicles.
            var pageCounter = new PageCounter(driver);
            var pageNum = pageCounter.pageNumChecker();  // check number of pages and return the number of pages
            
            // Click next page
            navigator.pageNum = pageNum;  // Set the property for the number of pages first


            for (int i = 1; i <= pageNum.searchResultsPageCount; i++ ) {
                
                // Call the datascraper and send through an argument for the class to search for.
                var dataScraper = new DataScraper(driver);
                dataScraper.GetHtml(tableHTMLtagToScrape);

                // Click the next page
                navigator.ClickNextPage(i);

            }










        }
    }
}

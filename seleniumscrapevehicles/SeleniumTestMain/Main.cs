using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Repository;
using DomainWideObjects.Settings;
using OpenQA.Selenium;
using SeleniumTestMain.General;
using SeleniumTestMain.General.Data;

namespace SeleniumTestMain {
    public class Main
    {
        
        // Tag to be scraped (inner html)
        private string tableHTMLtagToScrape = "t_main";
        private string tableSingleRowHtmlTagToScrape = "aj_view";

        //private string tableHTMLtagToScrape = "aj_out_poisk";
        private int searchSessionID;
        private int returnCode;

        
        //// Single search properties to set if needed
        //private bool manualSingleSearch = false;
        //private string singleVehicleToSearch = "DYNA";

        // multi vehicle search list
        private List<tblVehicle> vehicleSearchList;

     


        public void MainMethod()
        {
            //DbTest();


            Navigator navigator = new Navigator();
           // Instanciate objects in the navigator
            navigator.Create();

            vehicleSearchList = new List<tblVehicle>();


            ISearchTypeChooser searchTypeChooser = new SearchTypeChooser();

           vehicleSearchList = searchTypeChooser.ChooseTypeOfSearch(vehicleSearchList);


            // navigate to page
            navigator.NavigateToPage();
            // login to page - return the selenium driver into the var.
            var driver = navigator.LoginToPage();
            
            // Create Search Session
            var sessionCreator = new SessionCreator();
           searchSessionID = sessionCreator.CreateSearchSession();


            // Do a search for each vehicle read from the database.
            foreach (var item in vehicleSearchList)
            {
                 MainNavigationToLoop(navigator, item.Vehicle_Make, item.Vehicle_Model, item.Vehicle_CondtionFilter , driver, item.Vehicle_ID_Pk, item.Vehicle_ConditionCode);
            
            }
                
               CloseBrowserAndDispose(driver);
        }



        private void MainNavigationToLoop(Navigator navigator,  string vehicleMake, string vehicleModel,  bool? filterCondition  , IWebDriver driver, int vehicleID, double? vehicleCondition)
        {
            // Set current global search vehicle.

            AppSettings.setCurrentVehicle(vehicleID);

         
            // Begin foreach for all vehicles

            // Select Make
            IVehicleSelector vehicleSelector = new VehicleSelector(driver);
            vehicleSelector.SelectMake(vehicleMake);

            // Select Model
             returnCode = vehicleSelector.SelectModel(vehicleModel);
            if (returnCode == 1)
            {
                goto ENDTHISLOOP;
            }
            // Check if condition is to be filtered.
            var searchChecker = new SearchChecker();

            

            if (searchChecker.ConditionFiltered(filterCondition))
            {
                // Condition Picker
                var conditionPicker = new ConditionPicker(driver, vehicleCondition);
                // Click condition list
                conditionPicker.ClickConditions();
            }
            
       
           

           

            // Click Search button
            navigator.SearchButtonClicker(driver);



            // Check for the number of pages of the vehicles.
            var pageCounter = new PageCounter(driver);
            var pageNum = pageCounter.pageNumChecker(); // check number of pages and return the number of pages

            // Click next page
            navigator.pageNum = pageNum; // Set the property for the number of pages first

          


            if (pageNum.searchResultsPageCount > 1)
            {
                for (int i = 2; i <= pageNum.searchResultsPageCount; i++) {
                   Console.WriteLine("page number is greater than one so looping...");
                    // Call the datascraper and send through an argument for the class to search for.
                   // var dataScraper = new DataScraper(driver, vehicleID, searchSessionID);
                   // check for error code then exit
                    // returnCode = dataScraper.GetHtml(tableHTMLtagToScrape);
                    //if (returnCode == 1) {
                      // goto ENDTHISLOOP;

                    //}

                    IRowScraper rowScraper = new RowScraper(driver, vehicleID, searchSessionID);
                    // check for error code then exit
                    returnCode = rowScraper.GetSingleRowHtml(tableSingleRowHtmlTagToScrape);
                    if (returnCode == 999999) {
                        goto ENDTHISLOOP;

                    }
                    // NOW GRAB SINGLE ROWS OF DATA


                    // Click the next page
                    navigator.ClickNextPage(i);
                }
            }
            else
            {
                Console.WriteLine("Page number returned is one...");
                var dataScraper = new DataScraper(driver, vehicleID, searchSessionID);
                 returnCode = dataScraper.GetHtml(tableHTMLtagToScrape);
                if (returnCode == 1)
                {
                    goto ENDTHISLOOP;

                }
            }

            


        ENDTHISLOOP:;

        }


        private static void CloseBrowserAndDispose(IWebDriver driver) {
            driver.Close();
            driver.Dispose();
        }

     
    }
}

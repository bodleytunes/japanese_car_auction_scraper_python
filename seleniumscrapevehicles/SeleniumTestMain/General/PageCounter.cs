using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects;
using OpenQA.Selenium;
//using OpenQA.Selenium.Support.UI;
//using OpenQA.Selenium.Support.Events;

namespace SeleniumTestMain.General {
    class PageCounter
    {
        private IWebDriver driver;
        private int pageNum;

        // Construct
        public PageCounter(IWebDriver driver)
        {

            this.driver = driver;

        }

        public SearchResults pageNumChecker() {
            int pageNumCounted = 1;
            pageNum = 1;



            // proper while
            while (CheckForNextPage()) {
                pageNumCounted = pageNum;
                Console.WriteLine(pageNumCounted);
                // increment page number to see if it exists.
                pageNum++;
            }

            // Store the number of pages and return.
            return StorePageNum();

           

        }
        // Create instance of searchresults class and store the search count.
        private SearchResults StorePageNum()
        {
            var searchResults = new SearchResults() {searchResultsPageCount = pageNum};
            return searchResults;

        }

        public bool CheckForNextPage() {
            // Wait for element
           //  driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 15));


            try {
               
                driver.FindElement(By.XPath("//a[@onclick='navi(this," + pageNum + ");']"));

                return true;
            } catch (Exception e) {
                // not found!!

                return false;
            }




        }
    }
}

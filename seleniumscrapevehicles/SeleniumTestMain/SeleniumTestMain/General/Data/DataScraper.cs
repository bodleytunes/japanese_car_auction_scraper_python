using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenQA.Selenium;

namespace SeleniumTestMain.General.Data {
    class DataScraper : IDataScraper {
        #region IDataScraper Members

        private IWebDriver driver;
        private List<String> htmlList; 

        // Constructor
        public DataScraper(IWebDriver driver)
        {
            this.driver = driver;
            htmlList = new List<string>();

        }

        public void GetHtml(string tagToSearch) {
            // Wait for element
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));
            
            IWebElement tableElement = driver.FindElement(By.ClassName(tagToSearch));

            string tableElementHTML =
                (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableElement);

            Console.WriteLine(tableElementHTML);
           

            AddHTMLtoList(tableElementHTML);

        }

        private void AddHTMLtoList(string tableElementHTML)
        {
           // Add the scraped html to the list.
            htmlList.Add(tableElementHTML);

        }

        

        #endregion
    }
}

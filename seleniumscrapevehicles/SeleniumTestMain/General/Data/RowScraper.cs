using System;
using System.Collections.Generic;
using System.Collections.ObjectModel;
using System.Linq;
using System.Text;
using System.Web;
using OpenQA.Selenium;
using DomainWideObjects.DataAccess.Repo;
using DomainWideObjects.DataAccess;

namespace SeleniumTestMain.General.Data {
    public class RowScraper : IRowScraper
    {

        private IWebDriver driver;
        private int searchSessionID;
        private string rowElementHTML;
        private IWebElement tableRowElement;

       
        private int vehicleID;


        // Construct
        public RowScraper(IWebDriver driver, int vehicleID, int searchSessionId)
        {
            this.driver = driver;
            this.searchSessionID = searchSessionId;
            this.vehicleID = vehicleID;

        }


        

        public int GetSingleRowHtml(string tagToSearch)
        {
            for (int i = 0; i < 20; i++)
            {
                
         
                if (CheckElementExists(tagToSearch, i)) {
                    rowElementHTML =
                   (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableRowElement);

                   
                    string encodedHtml = HttpUtility.HtmlEncode("<table class=\"t_main\" cellpadding=\"0\" cellspacing=\"0\">");

                    rowElementHTML = HttpUtility.HtmlDecode(encodedHtml) + rowElementHTML;

                    // get all the text data 
                   // TextData(i);


                   /* // Console.WriteLine("Writing Row Element Data! ******" + rowElementHTML + "*************");
                    Console.WriteLine("Written data aj_view" + i);*/

                    
                    // Save to DB
                    ///////
                    var dbWriter = new DBWriter();
 
                    dbWriter.SaveHtmlRowToDB(rowElementHTML, searchSessionID, vehicleID);


                    // return 0;
                }
                else
                {
                    return 1;
                }


             

            }

            Console.WriteLine("***FINISHED SCRAPING SINGLE ROWS***");
           // Console.ReadLine();

            // error 1 not found so go back to beginning of loop.
            return 1;

          
        }

        private void TextData(int i) {
            // Scrape Text Data
            //  (Lotnumber)

            var tagList = new List<string>();
            tagList.Add("my_bids");
           // tagList.Add("color:#a93f15");
           // tagList.Add("tag3");

            foreach (string tag in tagList)
            {
                ScrapeTextData(tag, i);
            }

          

        }

        private void ScrapeTextData(string dataTag, int i) {
          

          
            // Get table
            IWebElement table = driver.FindElement(By.ClassName("t_main"));
            // Get Rows
     
                var rows = new ReadOnlyCollection<IWebElement>(table.FindElements(By.ClassName(dataTag))); 
           

      

            // Console.WriteLine(rows[i].Text);
           










        }


        public bool CheckElementExists(string tagToSearch, int i)
        {
            // Wait for element (was 10)
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 20));

            bool tableElementExists = false;
            try {
                // Can crash here if filtering the conditions results in nothing found.
                tableRowElement = driver.FindElement(By.Id(tagToSearch + i));
                tableElementExists = true;
                // was 18
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 7));

                return tableElementExists;
            } catch (Exception e) {
                // not found
                tableElementExists = false;
                // was 18
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 7));

                return tableElementExists;
            }
        }



    }
}

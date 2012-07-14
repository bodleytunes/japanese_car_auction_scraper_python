using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Castle.Core;
using Castle;

using OpenQA.Selenium;
using OpenQA.Selenium.IE;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Chrome;
using System.Diagnostics;
using DomainWideObjects;
using SeleniumTestMain.General;


namespace SeleniumTestMain
{
    internal interface INavigatable
    {
        void Create();
        void Finish();
        void NavigateToPage();
    }

    internal class Navigator : INavigatable
    {
        private string navUri;
        private IWebDriver driver;


        private SiteConfigurator siteConfig;
        private Website website;
        public SearchResults pageNum;
        private int currentPageNum = 1;

        public bool isLogin = true;



       



        public void Create()
        {
            
            driver = new ChromeDriver();
            //instanciate the website class.
            website = new Website();

            // Instanciate site configuration class.
            siteConfig = new SiteConfigurator(website);




        }




        public void NavigateToPage()
        {


            driver.Navigate().GoToUrl("http://www.jpcenter.ru");

        }

        public IWebDriver LoginToPage()
        {

            if (isLogin) {

                Authenticator authenticator = new Authenticator(website, driver);
                // Call the authenticate method.
                authenticator.Authenticate();

                // return the webdriver object
                return driver;

            }

            return driver;

            


        }

        public void SearchButtonClicker(IWebDriver driver) {

            try
            {
                //Get the search button into an element (webelement).
                IWebElement searchButton = driver.FindElement(By.Id("i_but3_sch"));
                // Send enter key to the search button so it doesnt timeout.
                searchButton.Click();


            } catch (Exception) {

                // not found!!
                

            }

            

        }

        public void ClickNextPage(int i)
        {
            
            if (pageNum.searchResultsPageCount > 1)
            {
                if (i < pageNum.searchResultsPageCount)
                {
                  // do something if more than one page
                    //currentPageNum++; // increment page number and then click it.

                   bool isClicked = ClickPage(i);
                    

                }
                

            }
            else
            {
                Console.WriteLine("nothing to click"); 

                // Search for next vehicle.
            }
            


        }

        private bool ClickPage(int currentPageNum) {
            try
            {
                // set longer timeout to wait before clicking element. (was set to 40
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 17));
                driver.FindElement(By.XPath("//a[@onclick='navi(this," + currentPageNum + ");']")).Click();
                return true;
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 1));
            }catch(Exception)
            {
                return false;
            }
        }





        public void Finish()
        {
            driver.Close();

        }



    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using Castle.Core;
using Castle;

using OpenQA.Selenium;
using OpenQA.Selenium.IE;
using OpenQA.Selenium.Firefox;
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



       



        public void Create()
        {
            driver = new FirefoxDriver();
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

            Authenticator authenticator = new Authenticator(website, driver);
            // Call the authenticate method.
            authenticator.Authenticate();

            // return the webdriver object
            return driver;


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
                // set longer timeout to wait before clicking element.
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 40));
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

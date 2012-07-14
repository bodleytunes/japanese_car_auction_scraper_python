using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

using OpenQA.Selenium;
using OpenQA.Selenium.IE;
using OpenQA.Selenium.Firefox;
using System.Diagnostics;
using DomainWideObjects;


namespace SeleniumTestMain {
    public class Authenticator : IAuthenticatable
    {
        public string username { get; set; }
        public string password { get; set; }
        private Website website;
        private IWebDriver driver;

        public Authenticator(Website website, IWebDriver driver)
        {

            this.website = website;
            this.driver = driver;


        }


        public void Authenticate()
        {
            
            // Click login
            driver.FindElement(By.CssSelector("input.i_but3.i_but3_ff")).Click();
            
            // enter username
            driver.FindElement(By.Name("username")).Clear();
            driver.FindElement(By.Name("username")).SendKeys(website.username);
            // enter password
            driver.FindElement(By.Name("password")).Clear();
            driver.FindElement(By.Name("password")).SendKeys(website.password);
            
            // click login
            driver.FindElement(By.CssSelector("input.ajneo3")).Click();


        }

    }
}

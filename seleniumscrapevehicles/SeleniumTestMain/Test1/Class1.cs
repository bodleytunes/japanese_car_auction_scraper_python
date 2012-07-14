using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using NUnit.Framework;
using OpenQA.Selenium;
using OpenQA.Selenium.Firefox;
using OpenQA.Selenium.Interactions;
using System.Diagnostics;


namespace Test1 {
    [TestFixture]
    public class Test1
    {

        private IWebDriver driver;
        private string make = "TOYOTA";
        private string model = "HIACE VAN";
        [Test]
        public void Test()
        {
            driver = new FirefoxDriver();
            driver.Navigate().GoToUrl("http://www.jpcenter.ru");
            driver.FindElement(By.PartialLinkText(make)).Click();
            driver.FindElement(By.PartialLinkText(model)).Click();
            // Wait for element
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));

            // Grab the element and then feed it to the actions statement below.
            IWebElement element = driver.FindElement(By.XPath("//div[@id='aj_sl1']/div[2]/img"));
            IWebElement element2 = driver.FindElement(By.Id("aj_sl1"));
         
            Actions actionsProvider = new Actions(driver);
            actionsProvider.DragAndDropToOffset(element, -100, -100);
            actionsProvider.DragAndDropToOffset(element2, -100, -100);
            
           

        }

      
        public void DragSlider() {
            // Wait for element
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));

            // Grab the element and then feed it to the actions statement below.
            IWebElement element = driver.FindElement(By.XPath("//div[@id='aj_sl1']/div[2]/img"));

            Console.WriteLine(element.ToString());
            Console.ReadLine();

            Actions actionsProvider = new Actions(driver);
            actionsProvider.DragAndDropToOffset(element, 50, 0);

            actionsProvider.ClickAndHold(element);
            actionsProvider.MoveByOffset(50, 0);
            actionsProvider.Release(element);


        }
    }
}

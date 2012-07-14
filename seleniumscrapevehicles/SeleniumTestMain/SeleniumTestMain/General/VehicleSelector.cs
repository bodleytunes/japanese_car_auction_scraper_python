using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenQA.Selenium;
using OpenQA.Selenium.IE;
using OpenQA.Selenium.Firefox;
using System.Diagnostics;
using OpenQA.Selenium.Interactions;
using SeleniumTestMain;
using NUnit.Framework;
using DomainWideObjects;
using System.Timers;


namespace SeleniumTestMain.General {
   
    public class VehicleSelector : IVehicleSelector
    {
        private IWebDriver driver;
        private string make = "TOYOTA";
        private string model = "HIACE VAN";

        // construct
    
        public VehicleSelector(IWebDriver driver)
        {
            this.driver = driver;
        }

        #region IVehicleSelector Members

       
        public void SelectMake()
        {
            // CHECK MAKE IS THERE
            bool isMakePresent = CheckMakeIsPresent(make);
            
            //Console.WriteLine("Is the Toyota present? " + isMakePresent.ToString());
            //Console.ReadLine();
            if(isMakePresent)
            {
                driver.FindElement(By.PartialLinkText(make)).Click();
            
            }
            else
            {
                Console.WriteLine("poopykins no make!!! :-(");
                Console.ReadLine();
                // try another make ??
            }

            

        }

    

        public void SelectModel() {
           // Check model is there
           bool isModelPresent = CheckModelIsPresent(model);
           
            Console.WriteLine("Is the Model present? " + isModelPresent.ToString());
          

            if(isModelPresent)
            {
                Console.WriteLine("clicking the model...");
               
                driver.FindElement(By.PartialLinkText(model)).Click();
            }
            else
            {
                Console.WriteLine("Oh No!  No model! ... ");
               

            }

        }
        
       

      

       


        private bool CheckModelIsPresent(string model) {
            try
            {
                driver.FindElement(By.PartialLinkText(model));
                return true;
            }
            catch (Exception)
            {
                
               // not found!!
                return false;

            }
        }

        private bool CheckMakeIsPresent(string make) {
            try {
                driver.FindElement(By.LinkText(make));
                return true;  // Success!
            } catch (Exception) {
                // not found!
                return false;

            }
        }

        #endregion
    }
}

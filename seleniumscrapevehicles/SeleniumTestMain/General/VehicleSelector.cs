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

using DomainWideObjects;
using System.Timers;


namespace SeleniumTestMain.General {
   
    public class VehicleSelector : IVehicleSelector
    {
        private IWebDriver driver;
       

        // construct
    
        public VehicleSelector(IWebDriver driver)
        {
            this.driver = driver;
        }

        #region IVehicleSelector Members

       
        public void SelectMake(string make)
        {
            // CHECK MAKE IS THERE
            bool isMakePresent = CheckMakeIsPresent(make);
            
            //Console.WriteLine("Is the Toyota present? " + isMakePresent.ToString());
            //Console.ReadLine();
            if(isMakePresent)
            {
                if(isPartialLinkClick(make))
                {
                    try 
                        { 
                        
                            driver.FindElement(By.PartialLinkText(make)).Click(); 
                    
                        }
                    
                    catch(Exception e){
                            
                    }

                }else
                {
                    driver.FindElement(By.LinkText(make)).Click();
                }

                
            
            }
            else
            {
                Console.WriteLine("no make!!! :-(");
                // Console.ReadLine();
                // try another make ??
            }

            

        }

    

        public int SelectModel(string model) {
           // Check model is there
           bool isModelPresent = CheckModelIsPresent(model);
           
            Console.WriteLine("Is the Model present? " + isModelPresent.ToString());


            if (CheckModelIsPresent(model))
            {
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 20));
                Console.WriteLine("clicking the model...");
                if (isPartialLinkClick(model)){
                    Console.WriteLine("clicking PARTIAL link text...");
                    driver.FindElement(By.PartialLinkText(model)).Click();
                    return 0;

                }

                Console.WriteLine("clicking link text...");
                    driver.FindElement(By.LinkText(model)).Click();
                    return 0;
                
          
                

            }
          
           
                Console.WriteLine("Oh No!  No model! ... ");

                return 1;

       

        }

        private bool isPartialLinkClick(string input) {
            switch (input)
            {
                case "FORD":
                    return false;
                 default:
                    return true;
                    
            }
        }
        
       

      

       


        private bool CheckModelIsPresent(string model) {
            driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 5));
            try
            {
                driver.FindElement(By.PartialLinkText(model));
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));
                return true;
            }
            catch (Exception)
            {
                driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 45));
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

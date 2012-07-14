using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using OpenQA.Selenium;

namespace SeleniumTestMain.General {
    class ConditionPicker
    {
        private IWebDriver driver;
        private string tagToSearch = "ajr";
        private List<double> conditionList; 

        public ConditionPicker(IWebDriver driver)
        {
            this.driver = driver;
            conditionList = new List<double>(){3, 3.5 , 4 , 4.5};


        }

        //public void buildConditions()
        //{
        //    conditionList.Add(3);
        //    conditionList.Add(3.5);
        //    conditionList.Add(4);
        //    conditionList.Add(4.5);

        //}

        public void ClickConditions()
        {
           
            foreach(double condition in conditionList)
            {
                try
                {
                    driver.FindElement(By.LinkText(condition.ToString())).Click();
                }
                catch (Exception)
                {
                    
                    
                }
                
            }

        }
    }
}

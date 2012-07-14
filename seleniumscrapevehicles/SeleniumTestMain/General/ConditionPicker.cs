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
        private List<double?> conditionList;
        private List<double> conditionsToSearch;

        public ConditionPicker(IWebDriver driver, double? conditionGrade)
        {
            this.driver = driver;
            
            if (conditionGrade == 1000)
            {
                conditionList = new List<double?>() { 3, 3.5, 4, 4.5 };
            }
            else
            {
                conditionList = new List<double?>();
                conditionList.Add(conditionGrade);
            }
            


        }

      

        public void ClickConditions()
        {

            CheckWhichConditionsArePresent();
            ClickOnConditions();



        }

        private void ClickOnConditions() {
            foreach (double condition in conditionsToSearch)
            {
                try
                {
                    // Wait for element
                    driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 5));
                    driver.FindElement(By.LinkText(condition.ToString())).Click();

                    // Wait for element (was set to 45 / was 17)
                    driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 10));


                }
                catch (Exception)
                {

                   
                }

            }
        }

        private void CheckWhichConditionsArePresent() {

            conditionsToSearch = new List<Double>();
            conditionsToSearch.Clear();


            foreach (double condition in conditionList) {
             
                try {
                   driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 5));
                
                    //driver.FindElement(By.LinkText(condition.ToString())).Click();
                    driver.FindElement(By.LinkText(condition.ToString()));
                    conditionsToSearch.Add(condition);
                    Console.WriteLine("Adding condition " + condition + " to search list");

                    driver.Manage().Timeouts().ImplicitlyWait(new TimeSpan(0, 0, 5));

                } catch (Exception) {

                    Console.WriteLine("Condition not found" + condition.ToString());
                   

                }

            }
        }
    }
}

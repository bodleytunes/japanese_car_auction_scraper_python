using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SeleniumTestMain {
   public class SearchChecker {


       // check if condition filtering is checked

       public bool ConditionFiltered(bool? filterCondition)
       {
           if (filterCondition == null)
           {
               return true;
           }
           if (filterCondition == false)
           {
               return false;
           }
           if (filterCondition == true)
           {
               return true;
           }

           return true;



       }
    }
}

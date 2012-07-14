using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Repo;

namespace SeleniumTestMain.General.RegexFinder {
   public class DataGetter {

       public IQueryable<DataRow> getRow()
       {
           var ctx = new seleniumScrapeEntities();


           var query = from hr in ctx.tblHtmlRows
                       where hr.Search_Session_ID_fk == 500
                       select new DataRow()
                                  {
                                      id = hr.html_row_id_PK,
                                      dataRowHtml = hr.html_row_data
                                  };

           return query;

       }

      /* private int? getLatestSearchSession()
       {

           var ctx = new seleniumScrapeEntities();
           
           var ss = from db in ctx.tblSearchSessions

 
                      

           
       }
       */
 
    }
}

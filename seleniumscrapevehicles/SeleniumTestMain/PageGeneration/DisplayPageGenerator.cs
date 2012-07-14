using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Entities;
using DomainWideObjects.DataAccess.Repository;

namespace SeleniumTestMain.PageGeneration {
   public class DisplayPageGenerator
   {
       private DisplayPage page;


       // Change the session (3) to a selectable variable as soon as ready for production.
       public void CreateNewPage()
       {
           var sessionList = GetHTMLdata().ToList();

           page = new DisplayPage();

           page.searchSession = sessionList[3].Search_Session_ID_PK;
          
           var htmlEnum = from h in sessionList[3].tblHtmls
                       where h.Search_Session_ID_fk == 3
                       select h.html_data;
          
           var htmlList = htmlEnum.ToList();


          
           
               var timeStampEnum = from h in sessionList[3].tblHtmls
                                  where h.Search_Session_ID_fk == 3
                                  select h.Search_Date_Timestamp;

           var timeStampList = timeStampEnum.ToList();

          





       }

       public IQueryable<tblSearchSession> GetHTMLdata()
       {
           var dbReader = new DBreader();

           var sessionList = dbReader.GetAllHTMLbySearchSession(3);

           return sessionList;

       }

   }
}

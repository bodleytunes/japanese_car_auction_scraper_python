using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;

namespace SeleniumTestMain.General.Data {
   public class SessionCreator {

       public int CreateSearchSession() {
           var searchSession = new tblSearchSession()
                                   {
                                       Search_Session_Timestamp = DateTime.Now

                                   };
           
           // add search session to db
           int searchSessionID = AddSearchSessionToDb(searchSession);

           return searchSessionID;

       }

       private int AddSearchSessionToDb(tblSearchSession searchSession) {
           var dbWriter = new DBWriter();
           int searchSessionID = dbWriter.InsertSearchSession(searchSession);
           return searchSessionID;
       }
    }
}

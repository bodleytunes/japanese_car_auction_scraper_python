using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess.Entities;

namespace DomainWideObjects.DataAccess.Repository {
   public class DBreader {


       public List<tblVehicle> readSearchVehicles()
       {
           var db = new seleniumScrapeEntities();

           var vehicles = from v in db.tblVehicles
                          where v.Vehicle_WillBeSearched == true
                          select v;

           var vehicleList = vehicles.ToList();


           return vehicleList;


       }

       public IQueryable<tblSearchSession> GetAllHTMLbySearchSession(int searchSessionID)
       {
           var db = new seleniumScrapeEntities();

           var html = from s in db.tblSearchSessions
                      from h in db.tblHtmls
                      where s.Search_Session_ID_PK == 3
                      select s;                           
                               

           return html;
       }


        public List<tblVehicle> GetSingleSearchVehicle(string vehicleModelToSearch)
        {
            var db = new seleniumScrapeEntities();
            
            var vehicles = from v in db.tblVehicles
                           where v.Vehicle_Model == vehicleModelToSearch
                          select v;

           var vehicleList = vehicles.ToList();


           return vehicleList;
        }

       public void TestQuery()
       {

           var db = new seleniumScrapeEntities();

           var sessionCount = (from s in db.tblSearchSessions
                               select s).Count();



           var sessionData = from h in db.tblSearchSessions
                             from s in h.tblHtmls
                             where s.Search_Session_ID_fk == sessionCount
                             select s;


           var filterVehicle = from s in sessionData

                               where s.Vehicle_id_fk == 7
                               select s;
				  

       }
       
       

      


   }
}

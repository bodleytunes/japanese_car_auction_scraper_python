using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Repo;
using DomainWideObjects.DataAccess.Repository;
using MongoDB.Bson;
using MongoDB.Driver;


namespace SeleniumTestMain.General.Data
{
    public class DBWriter
    {


        public int InsertSearchSession(tblSearchSession searchSession)
        {

            // Create database context.
            var ctx = new seleniumScrapeEntities();

            ctx.tblSearchSessions.AddObject(searchSession);
            ctx.SaveChanges();

            return searchSession.Search_Session_ID_PK;
        }


        public void SaveHtmlRowToDB(string rowElementHTML, int searchSessionId, int vehicleId)
        {

            /*var ctx = new seleniumScrapeEntities();

            var htmlRow = new tblHtmlRow
                              {
                                  html_row_data = rowElementHTML,
                                  // get latest tblHtml ID pk (this is the fk)
                                  // html_data_id_fk = GetHtmlTableId(),
                                  Search_Date_Timestamp = DateTime.Now,


                                  Vehicle_id_fk = vehicleId,
                                  Search_Session_ID_fk = searchSessionId

                              };



            var repo = new Repo(ctx);

            repo.Add(htmlRow);

            repo.SaveChanges<tblHtmlRow>();*/

            // Do Mongo DB stuff

            var mongoOps = new MongoOps();
            mongoOps.DoMongo(searchSessionId, vehicleId, rowElementHTML);




        }

        private int GetHtmlTableId()
        {
            var ctx = new seleniumScrapeEntities();

            var htmlTableId = (from h in ctx.tblHtmls
                               where h.html_id_pk > 0
                               orderby h.html_id_pk descending
                               select h.html_id_pk).FirstOrDefault();

            return htmlTableId;

        }


    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using DomainWideObjects.Settings;
using MongoDB.Driver;
using MongoDB.Bson;
using MongoDB.Driver.Builders;
using MongoDB.Driver.Wrappers;
using MongoDB.Bson.IO;



namespace DomainWideObjects.DataAccess.Repository {
    class MongoOps
    {
        
        private List<AuctionVehicleHtmlRow> htmlData;
        
        public void DoMongo(int searchSessionId, int vehicleId, string rowElementHtml)
       {
           
           var AuctionVehicles = ConnectToMongo();

           var vehicles = GetMongoCollection(AuctionVehicles);

         //  var vehicleData = GetVehicleData(vehicleId);

           //DoHtmlRows(rowElementHtml);


           var newVehicle = CreateVehicle(searchSessionId, rowElementHtml);
            
           SaveMongo(AuctionVehicles, vehicles, newVehicle);


// Get Session variables!

           // GetSession(181);



       }

        public void DoHtmlRows(string rowElementHtml) {
            
            // Remember to instanciate the collection of auction vehicle rows before adding!
           htmlData = new List<AuctionVehicleHtmlRow>();


            htmlData.Add(new AuctionVehicleHtmlRow()
            {
                // Run methods to return html row data
                htmlRow = rowElementHtml
            });
           


        }

        public List<AuctionVehicleHtmlRow> GetHtmlRowsForMongo()
        {
            
            return htmlData;

        } 

        public static Vehicle GetVehicleData(int vehicleId)
        {
//Get vehicle make / model

            var context = new seleniumScrapeEntities();

            IQueryable<string> makeQuery = from v in context.tblVehicles
                            where v.Vehicle_ID_Pk == vehicleId
                            select v.Vehicle_Make;

            var makeList = makeQuery.ToList();

          

            IQueryable<string> modelQuery = from db in context.tblVehicles
                             where db.Vehicle_ID_Pk == vehicleId
                             select db.Vehicle_Model;

            var modelList = modelQuery.ToList();

            var vehicleData = new Vehicle()
                                  {
                                      vehicleMake = makeList[0],
                                      vehicleModel = modelList[0]
                                  };

            return vehicleData;


        }

        private void SaveMongo(MongoDatabase AuctionVehicles, MongoCollection vehicles, AuctionVehicle newVehicle)
       {
           Console.WriteLine("Inserting into MONGODB!!!!!!!!");

            vehicles.Insert(newVehicle);

            Console.WriteLine("** MongoDB Insert Complete **");

       }

       private MongoCollection GetMongoCollection(MongoDatabase AuctionVehicles)
       {
           MongoCollection vehicles;

           vehicles = AuctionVehicles.GetCollection("vehicles");

            // returns the collection / table from mongo db.
           return vehicles;

       }

       private AuctionVehicle CreateVehicle(int searchSessionId, string rowElementHtml)
       {
          
          

           var newVehicle = new AuctionVehicle();
           
           //newVehicle._id = System.Guid.NewGuid().ToString();
           newVehicle._searchSession = searchSessionId;
           // Set the current search vehicle based on the current one being search (global)
           newVehicle.make = AppSettings.globalMake;
           newVehicle.model = AppSettings.globalModel;
           newVehicle.searchSessionTimeStamp = DateTime.Now;
           newVehicle.htmlData = new List<AuctionVehicleHtmlRow>();
           newVehicle.htmlData.Add(new AuctionVehicleHtmlRow()
                                       {
                                           htmlRow = rowElementHtml
                                       });

           newVehicle.inPostgres = false;
           

           return newVehicle;


       }

       private MongoDatabase ConnectToMongo()
       {
           MongoServer server = MongoServer.Create("mongodb://jmcmongo");

           MongoDatabase Auctionvehicles = server.GetDatabase("Auctionvehicles");

           return Auctionvehicles;
           
       }

        private void GetSession(int sessionId)
        {
           
          // Get the database instance of mongo
           var AuctionVehicles = ConnectToMongo();

         // Get mongo Collection of documents, return them as a type of pre-made object (auction vehicle)
            // param that is passed in is the string for the collection name (Vehicles)
           var collection = AuctionVehicles.GetCollection<AuctionVehicle>("vehicles");

            ///
            /// This searches for the searchsession 181
            /// 
            var query = new QueryDocument("_searchSession", 181);

            

            ///
            /// This one gets all
           var cursor = collection.FindAllAs<AuctionVehicle>();

            ///
            ///  This one gets one from using the above query.
            /// 
          // var cursor = collection.Find(query);

           // Set returned cursor's sort params (sort by search session id decending).
         
           cursor.SetSortOrder(SortBy.Descending("_searchSession"));

            // Set limit of returned documents.
            cursor.SetLimit(1);

            // Convert the cursort to a list so can enumerate.
            var list = cursor.ToList();

            // Get the latest search session (first session in the list)
            int latestSession = list[0]._searchSession;

            // this one works for ANDS
            var biggerQuery = Query.And(
                Query.EQ("make", "TOYOTA"),
                Query.EQ("model", "HIACE VAN")
                
                );

            // This one works for ORs
            var queryOr = Query.Or(
                Query.EQ("model", "SAFARI"),
                Query.EQ("model", "ASTRO"),
                Query.EQ("model", "CHEVYVAN")
                );

            // Create regex for mongo wildcard search
            var regex = new BsonRegularExpression("/.*" + "USS Nagoya" + "*/");
            
            // This one works for ands and regex
            // This is my favourite way to query.  each one is an And and finally a regex to do wildcard text search  - remember the bsonregularexpression.
            var biggerQueryDocumentStyle = new QueryDocument()
                                               {
                                                   {"make", "TOYOTA"},
                                                   {"model", "HIACE VAN"},
                                                   {"htmlData.htmlRow", regex}
                                               };
            
            var cursor3 = collection.Find(biggerQueryDocumentStyle);
            
            var cursor2 = collection.Find(biggerQuery);
            
            var cursor3list = cursor3.ToList();
            
            var cursor2list = cursor2.ToList();
            /*
            foreach (var item in cursor2list) {
                Console.WriteLine(item.make + " " + item.model + " " + "Session ID = " + item._searchSession);
                Console.ReadLine();
            }

            foreach (var item in cursor3list) {
                Console.WriteLine(item.make + " " + item.model + " " + "Session ID = " + item._searchSession);
                Console.ReadLine();
            }


/*
 * 
            foreach (var item in list)
            {
                Console.WriteLine(item.make + " " + item.model + " " + "Session ID = " + item._searchSession);
                Console.ReadLine();
            }
 */

            




        } 

       


    }

    

    }

public class AuctionVehicle
    {
        public MongoDB.Bson.ObjectId _id { get; set; }
        public int _searchSession { get; set; }
        public DateTime searchSessionTimeStamp { get; set; }
        
        public string make { get; set; }
        public string model { get; set; }

        public List<AuctionVehicleHtmlRow> htmlData { get; set; }

        public int numberOfVehicles { get; set; }

        public Boolean inPostgres { get; set; }

    }

    public class AuctionVehicleHtmlRow
    {
        public string htmlRow { get; set; }
    }

public class Vehicle{

    public string vehicleMake { get; set; }
    public string vehicleModel { get; set; }
}

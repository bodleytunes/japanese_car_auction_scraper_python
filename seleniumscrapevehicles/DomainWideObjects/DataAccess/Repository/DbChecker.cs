using System;
using System.Collections.Generic;
using System.Data.Objects;
using System.Linq;
using System.Text;
using DomainWideObjects.DataAccess;

namespace DomainWideObjects.DataAccess.Repository {
    public class DbChecker<T> where T : class
    {

        private ObjectContext _context;
        private IObjectSet<T> _objectSet;

        // Constructor
        public DbChecker()
            : this(new seleniumScrapeEntities())
        {

        }

        /// <summary>
        /// Initializes a new instance of the DataRepository class
        /// </summary>
        /// <param name="context">The Entity Framework ObjectContext</param>
        public DbChecker(ObjectContext context)
        {
            _context = context;
            _objectSet = _context.CreateObjectSet<T>();
        }

        public void AddNewVehicle()
        {

            string vehicleMake = "TOYOTA";
            string vehicleModel = "HIACE VAN";

            string country = "Japanese";
            string defined = "Super Robinson";
            string general = "campertronic";

           

            if (!CheckVehicleExists(vehicleMake, vehicleModel))
            {
                bool countryExists = CheckCountryExists(country);
                bool definedExists = CheckDefinedTypeExists(defined);
                bool generalExists = CheckGeneralTypeExists(general);
                // Create new vehicle object.
                var vehicle = new tblVehicle();
                vehicle.Vehicle_Make = "Toyota";
                vehicle.Vehicle_Model = "Camroad";


                if (countryExists)
                {

                    SelectExistingCountry(vehicle, "Japanese");


                }
                else
                {
                    // Create new country
                }

                if (generalExists)
                {
                    var db2 = new seleniumScrapeEntities();

                    // Set the Vehicle Defined Type FK (in vehicle table)
                   SelectExistingGeneralType(vehicle, "Camper");
                }
                else
                {
                    // Create new Defined Type.
                }
                if (definedExists)
                {
                  SelectExistingDefinedType(vehicle, "MonsterCar");
                }
                else
                {
                    // Create new general type.
                }
            }




        }

        private void SelectExistingCountry(tblVehicle vehicle, string country)
        {
            var db2 = new seleniumScrapeEntities();

          

            // Set the Vehicle Country of Origin FK (in vehicle table)
            vehicle.Vehicle_Type_ID_fk =
                db2.tblVehicleTypeCountries.Where(x => x.Vehicle_Type_Country == country).Select(
                    x => x.Vehicle_Type_Country_ID_pk).SingleOrDefault();

            db2.Dispose();
        }

        private void SelectExistingGeneralType(tblVehicle vehicle, string generalType) {
            var db2 = new seleniumScrapeEntities();



            // Set the Vehicle Country of Origin FK (in vehicle table)
            vehicle.Vehicle_Type_General_id_fk =
                db2.tblVehicleTypeGenerals.Where(x => x.VehicleTypeGeneral == generalType).Select(
                    x => x.VehicleTypeGeneral_pk).SingleOrDefault();

            db2.Dispose();
        }

        private void SelectExistingDefinedType(tblVehicle vehicle, string definedType) {
            var db2 = new seleniumScrapeEntities();



            // Set the Vehicle Country of Origin FK (in vehicle table)
            vehicle.Vehicle_Type_Defined_fk =
                db2.tblVehicleTypeDefineds.Where(x => x.VehicleTypeDefined == definedType).Select(
                    x => x.VehicleTypeDefined_id_pk).SingleOrDefault();

            db2.Dispose();
        }

    private bool CheckVehicleExists(string vehicleMake, string vehicleModel) {
            var db = new seleniumScrapeEntities();

            //var query = db.tblVehicleTypeCountries.Where(x => x.Vehicle_Type == p);
            var query = db.tblVehicles.Where(x => x.Vehicle_Make == vehicleMake);
            query = db.tblVehicles.Where(x => x.Vehicle_Model == vehicleModel);


            if (query.Count() > 0) {
                return false;
            }



            return true; ;
        }

        private bool CheckGeneralTypeExists(string general) {
            var db = new seleniumScrapeEntities();

            var query = db.tblVehicleTypeGenerals.Where(x => x.VehicleTypeGeneral == general);

            if (query.Count() > 0) {
                return false;
            }



            return true;
        }

        private bool CheckDefinedTypeExists(string defined) {
            var db = new seleniumScrapeEntities();

            var query = db.tblVehicleTypeDefineds.Where(x => x.VehicleTypeDefined == defined);

            if (query.Count() > 0) {
                return false;
            }



            return true;
        }

        private bool CheckCountryExists(string p) {

            var db = new seleniumScrapeEntities();

            var query = db.tblVehicleTypeCountries.Where(x => x.Vehicle_Type_Country == p);

            if (query.Count() > 0) {
                return false;
            }



            return true;

        }




    }
}

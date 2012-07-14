using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DomainWideObjects.DataAccess {
    public class VehicleSaver {

        public void SaveToDB(tblVehicle vehicle)
        {

            var ctx = new seleniumScrapeEntities();

            ctx.tblVehicles.AddObject(vehicle);

            ctx.SaveChanges();


        }
    }
}

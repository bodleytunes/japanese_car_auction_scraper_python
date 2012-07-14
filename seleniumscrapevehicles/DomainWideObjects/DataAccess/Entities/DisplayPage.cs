using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DomainWideObjects.DataAccess.Entities {
    public class DisplayPage {
        
        public int searchSession { get; set; }
        public IEnumerable<DateTime> searchTimeStamp { get; set; }
        
        public List<string> vehicleMake { get; set; }
        public List<string> vehicleModel { get; set; }

        public List<string> html { get; set; } 
    }
}

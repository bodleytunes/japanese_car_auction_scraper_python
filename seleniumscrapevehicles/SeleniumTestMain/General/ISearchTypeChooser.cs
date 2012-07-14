using System.Collections.Generic;
using DomainWideObjects.DataAccess;

namespace SeleniumTestMain.General
{
    public interface ISearchTypeChooser
    {
        List<tblVehicle> ChooseTypeOfSearch(List<tblVehicle> vehicleSearchList);
    }
}
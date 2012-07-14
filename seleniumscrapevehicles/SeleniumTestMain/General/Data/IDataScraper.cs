using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace SeleniumTestMain.General.Data {
    interface IDataScraper
    {

        int GetHtml(string tagToSearch);

    }
}

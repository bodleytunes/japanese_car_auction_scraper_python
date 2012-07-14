using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.Web.UI;
using System.Web.UI.WebControls;
using DomainWideObjects.DataAccess;
using DomainWideObjects.DataAccess.Repository;
using System.Data.Entity;


namespace WebformsUI {
    public partial class _Default : System.Web.UI.Page {
        protected void Page_Load(object sender, EventArgs e)
        {

            var db = new DBreader();

            var htmlQueryable = db.GetAllHTMLbySearchSession(3);

            var htmlList = htmlQueryable.ToList();

           
          
         

            

        }
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace DomainWideObjects {
    public class SiteConfigurator : ISiteConfigurable, IAuthenticatable
    {
        private string _Url;
        private string _Username;
        private string _Password;


        public string url {
            get {
                return _Url;
            }
            set {
                _Url = value;
            }
        }

        

        #region IAuthenticatable Members

        public string username {
            get {
                return _Username;
            }
            set {
                _Username = value;
            }
        }

        public string password {
            get {
                return _Password;
            }
            set {
                _Password = value;
            }
        }

        public SiteConfigurator(Website website)
        {
            
            this.url = website.url;
            this.username = website.username;
            this.password = website.password;

        }

        #endregion
    }
}

using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;


namespace DomainWideObjects.DataAccess.Repo {
    public class Repo : IRepo
    {
        private seleniumScrapeEntities _ctx;

        // Constructor.  Pass in the entity context.
        public Repo(seleniumScrapeEntities ctx)
        {
            this._ctx = ctx;
        }

        public void Add<T>(T item)
        {
           

            // The GetSetName<T> method seems to get the correct type?
            // Then it adds the object
            _ctx.AddObject(GetSetName<T>(), item);

            

        }

        public void Delete<T>(T item)
        {
           

            _ctx.DeleteObject(item);
            
           
        }

        public void SaveChanges<T>()
        {
           

            _ctx.SaveChanges();

            
        }

        public string GetSetName<T>() {

            //If you get an error here it's because your namespace
            //for your EDM doesn't match the partial model class
            //to change - open the properties for the EDM FILE and change "Custom Tool Namespace"
            //Not - this IS NOT the Namespace setting in the EDM designer - that's for something
            //else entirely. This is for the EDMX file itself (r-click, properties)

            var entitySetProperty =

            _ctx.GetType().GetProperties()
               .Single(p => p.PropertyType.IsGenericType && typeof(IQueryable<>)
               .MakeGenericType(typeof(T)).IsAssignableFrom(p.PropertyType));

            return entitySetProperty.Name;
        }
    }
}

namespace DomainWideObjects.DataAccess.Repo
{
    public interface IRepo
    {
        void Add<T>(T item);
        void Delete<T>(T item);
        void SaveChanges<T>();
        string GetSetName<T>();
    }
}
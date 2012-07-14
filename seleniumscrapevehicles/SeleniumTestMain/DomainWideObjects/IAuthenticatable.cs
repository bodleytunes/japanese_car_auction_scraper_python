namespace DomainWideObjects
{
    public interface IAuthenticatable
    {
        string username { get; set; }
        string password { get; set; }
    }
}
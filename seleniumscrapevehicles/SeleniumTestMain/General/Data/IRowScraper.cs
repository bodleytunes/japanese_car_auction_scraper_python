namespace SeleniumTestMain.General.Data
{
    public interface IRowScraper
    {
        int GetSingleRowHtml(string tagToSearch);
        bool CheckElementExists(string tagToSearch, int i);
    }
}
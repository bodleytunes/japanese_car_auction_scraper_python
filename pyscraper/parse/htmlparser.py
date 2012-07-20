from BeautifulSoup import BeautifulSoup

def start_parse(row_data, row_html):
    
    # now with the single web element use .text to get a string of the text items delimeted by newlines \n
    # then just split by the new lines to get the separate cells!
    # old way to get html (for parsing) 
    # (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableElement);
    print(row_html)
    #raw_input(row_data.text)
    #row_list = row_data.text.split("\n")
    #for item in row_list:
    #    print item
        
    #print "======================="
    
   
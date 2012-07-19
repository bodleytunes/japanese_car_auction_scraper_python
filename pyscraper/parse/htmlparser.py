from BeautifulSoup import BeautifulSoup

def start_parse(row_data):
    
    # now with the single web element use .text to get a string of the text items delimeted by newlines \n
    # then just split by the new lines to get the separate cells!
    row_list = row_data.text.split("\n")
    for item in row_list:
        print item
        
    print "======================="
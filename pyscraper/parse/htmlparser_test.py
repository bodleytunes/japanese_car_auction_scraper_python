from bs4 import BeautifulSoup

def start_parse():
    
    # now with the single web element use .text to get a string of the text items delimeted by newlines \n
    # then just split by the new lines to get the separate cells!
    # old way to get html (for parsing) 
    # (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableElement);
    #print(row_html)
    
    file = open("snippets_to_scrape.html", "r")
    soup = BeautifulSoup(file)

    #raw_input(soup.prettify())
    
    lotnumber = soup.find("a", { "class" : "my_bids" })
    lotnumber_text = lotnumber.string
    #print lotnumber_text
    
    auction_house = soup.find_all("nobr")[1].string
    # got first half of auction house
    #print auction_house
    auction_house = auction_house.replace("\n","")  #remove newlines
    auction_house = auction_house.strip()           #remove whitespace
    auction_dict = {"USS Nag" : "USS NAGOYA", \
                    "CAA Nag" : "CAA NAGOYA", \
                    }
    #print auction_dict[auction_house]
    auction_house = auction_dict[auction_house]
    
    img_link_list = soup.find_all("a", {"class": "aj_resize"})
    
    img1 = img_link_list[0]["href"]  # get correct indices and then href key
    img2 = img_link_list[1]["href"]
    img3 = img_link_list[2]["href"]
    
    #print img1
    
    vehicle_link_list = soup.find_all("a", {"class" : "my_bids"})
    
    print vehicle_link_list[0]['href']
    vehicle_link = vehicle_link_list[0]['href']
    
    
    #//*[@id="aj_view3"]/td[4]    
        
    #raw_input("lotnumber = " + lotnumber_text)
    
   
    #f.write("lotnumber = " + lotnumber_text + "\n")
    #for link in soup.find_all('a'):
       # print(link.get('href'))
    
    #raw_input(row_data.text)
    #row_list = row_data.text.split("\n")
    #for item in row_list:
    #    print item
        
    #print "======================="

start_parse()
  
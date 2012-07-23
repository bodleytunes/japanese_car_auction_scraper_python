from bs4 import BeautifulSoup

def start_parse(row_data, row_html, f, auction_house_unique=None):
    
    # now with the single web element use .text to get a string of the text items delimeted by newlines \n
    # then just split by the new lines to get the separate cells!
    # old way to get html (for parsing) 
    # (String)((IJavaScriptExecutor)driver).ExecuteScript("return arguments[0].innerHTML", tableElement);
    #print(row_html)
    
    soup = BeautifulSoup(row_html)
    #raw_input(soup.prettify())
    
    lotnumber = soup.find("a", { "class" : "my_bids" })
    lotnumber_text = lotnumber.string
    #raw_input("lotnumber = " + lotnumber_text)
    auction_house = soup.find_all("nobr")[1].string
    # got first half of auction house
    #print auction_house
    auction_house = auction_house.replace("\n","")  #remove newlines
    auction_house = auction_house.strip()           #remove whitespace
    auction_dict = {"USS Nag" : "USS NAGOYA", \
                    "CAA Nag" : "CAA NAGOYA", \
                    }
    
  
    if auction_house not in auction_house_unique:
        auction_house_unique.append(auction_house)
    #raw_input(auction_house)
    #print auction_dict[auction_house]
    #auction_house = auction_dict[auction_house]
    
    img_link_list = soup.find_all("a", {"class": "aj_resize"})
    
    try:
        img1 = img_link_list[0]["href"]  # get correct indices and then href key
    except:
        "img1 problem"
    try:
        img2 = img_link_list[1]["href"]
    except:
        "img2 problem"
    try:
        img3 = img_link_list[2]["href"]
    except:
        "img3 problem"
    
    
    #print img1
    
    vehicle_link_list = soup.find_all("a", {"class" : "my_bids"})
    
    #print vehicle_link_list[0]['href']
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
    
   
    f.write("lotnumber = " + lotnumber_text + " " + auction_house + "\n")
    #for link in soup.find_all('a'):
    #    print(link.get('href'))
    
    #raw_input(row_data.text)
    #row_list = row_data.text.split("\n")
    #for item in row_list:
    #    print item
        
    #print "======================="
    for item in auction_house_unique:
        print item
    
    return auction_house_unique
    
  
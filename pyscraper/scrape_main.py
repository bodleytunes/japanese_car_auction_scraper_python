from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.keys import Keys
import time
from parse import htmlparser

scrape_url = "http://www.jpcenter.ru" #Url to scrape
 # Create instance of chrome driver.
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
login_user = "monkey5"
login_password = "bingo"
vehicle_make = "GM"
vehicle_model = "CHEVROLET ASTRO"
vehicles_to_search = []
xpath_login_box = "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/span/table/tbody/tr/td/input[2]"
css_login_ok = "ajneo3"

def begin():

    driver.get(scrape_url)
    
    authenticate()  #authenticate and login
    # Choose vehicle
    # Create vehicles to search list
    #vehicles_to_search.append(vehicle_to_search(vehicle_make, vehicle_model))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "HIACE VAN"))
    vehicles_to_search.append(vehicle_to_search("GM", "CORDOBA2"))
    vehicles_to_search.append(vehicle_to_search("GM", "CHEVROLET CHEVYVAN"))
    vehicles_to_search.append(vehicle_to_search("GMC", "ANY"))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "TOWNACE VAN"))
    vehicles_to_search.append(vehicle_to_search("ISUZU", "ELF TRUCK"))
    vehicles_to_search.append(vehicle_to_search("MAZDA", "BONGO FRIENDEE"))
    vehicles_to_search.append(vehicle_to_search("NISSAN", "CARAVAN"))
    vehicles_to_search.append(vehicle_to_search("MAZDA", "RX-7"))
    vehicles_to_search.append(vehicle_to_search("MUNGO", "PARROT"))
    vehicles_to_search.append(vehicle_to_search("MaNGO", "PARROT"))
    vehicles_to_search.append(vehicle_to_search("ISUZU", "RODEO"))
    vehicles_to_search.append(vehicle_to_search("MITSUBISHI", "DELICA TRUCK"))
    
    vehicle_stuff()

def authenticate():
    # Click login
    driver.find_element_by_xpath(xpath_login_box).click()
    # Enter Username and password
    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys(login_user)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(login_password)
    #Click login
    driver.find_element_by_class_name(css_login_ok ).click()
    
def vehicle_stuff():
    
    for search_vehicle in vehicles_to_search:
        time.sleep(3)  # Don't want to go too fast, give it a sleep to let things load.
        # Only continue to do the vehicle stuff if make & model is present! otherwise loop 
        # around to next vehicle in the list.  
        if(choose_make_link(search_vehicle.make) and choose_model(search_vehicle.model)):
            time.sleep(3)     
            
            count_pages()
#           row_count = count_rows()
#           get_rows(row_count, page_count)
          # Now click button to return to home screen (to select make)
            driver.find_element_by_class_name("aj_exp").click()        
        else:
                #if no model on page, then click home
            print("no model!")
            time.sleep(2)
            driver.find_element_by_class_name("nachalo").click()  # Click home
        print("finished vehicle" + " " + search_vehicle.make + search_vehicle.model)
        
## Loop starts here for each vehicle
    
def choose_make_link(make):
    try:
        driver.find_element_by_link_text(make).click()
        return 1
    except:
        print "full link error"
        return None
     
def choose_model(model):
    try:
        driver.find_element_by_partial_link_text(model).click()
        return 1
    except:
        return None
    
def count_pages():
    
    while (check_next_arrow_exists() or check_left_arrow_exists()):   # Check that either the left or right nav arrow for pages exists
        elements = driver.find_elements_by_class_name("navi1") #get all page number elements
        elements_unique = []  #create empty list for unique page numbers
        for element in elements:
            elements_unique.append(int(element.text)) #add to the new list as integer so can be sorted
            
        elements_unique = sorted(set(elements_unique))  # set makes unique, sort sorts the order
          
        page_count_run = len(elements_unique)  # total number of items in the list
        # if not right arrow then add one to the page count run otherwise it ends one too early
        if (check_next_arrow_exists()):
            page_count_run = page_count_run - 1 # minus one to get rid of the end high number page
          
        for i in range(1, page_count_run):
            #Get Rows!
            get_row_data()
            
            elements[i].click()
            # for some reason need to refresh the elements after a click or vanishes from DOM!
            elements = driver.find_elements_by_class_name("navi1")
            time.sleep(3)
        # Click next arrow
        if (check_next_arrow_exists()):   # Check that the right hand (next ) arrow exists
            driver.find_element_by_xpath("//span[@class='navi2'][contains(@style,'background-position:-110')]").click()
        else:
            break
         # loop around        
def check_next_arrow_exists():
    try:
        driver.find_element_by_xpath("//span[@class='navi2'][contains(@style,'background-position:-110')]")
        return True 
    except:
        return False
def check_left_arrow_exists():
    try:
        driver.find_element_by_xpath("//span[@class='navi2'][contains(@style,'background-position:-98')]")
        return True 
    except:
        return False    
def check_navi_dots(): # Check for BOTH navi dots
    try:
        driver.find_element_by_css_selector("b.navi_dots")
        driver.find_element_by_css_selector("td.navi_dots")
        return True 
    except:
        return False 

def get_row_data():
    # Find all aj elements(row elements) | also remember the not operator to ditch the header row aj_view00!    
    row_elements = driver.find_elements_by_xpath("//tr[contains(@id, 'aj_view')][not(contains(@id, 'aj_view00'))]")
    number_of_rows = len(row_elements)
    
    
    
    for row_element in row_elements:
        row_html = driver.execute_script("return arguments[0].innerHTML", row_element)
        htmlparser.start_parse(row_element, row_html)
        
                

def get_rows(row_count):
    print "get rows"

def parse_vehicles(vehicles):
    
    vehicles=[]
    vehicles.append(vehicle(make, model, year, miles, grade, date, start_price, end_price))
    # Do parsing stuff
    
    # Write to new list
    
    
    
    vehicles_parsed = clean_vehicles(vehicles)
    
    for vehicle in vehicles_parsed:
        save_to_db(vehicle)
        
def save_to_db(vehicle):
    
    #try / Catch
    db = GetDB()
    db.append(vehicle)
    db.flush()

##  Loop END here for each vehicle    
    
def finish():
        
    driver.quit()
    
class vehicle():
    
    def __init__(self,lotnumber=None,make=None,model=None,year=None,miles=None,\
                 grade=None,date=None,start_price=None,end_price=None):
        
        self.lotnumber=lotnumber
        self.make=make
        self.model=model
        self.year=year
        self.miles=miles
        self.grade=grade
        self.date=date
        self.start_price=start_price
        self.end_price=end_price
        
class vehicle_to_search():
    def __init__(self, make=None, model=None):
        self.make=make
        self.model=model
        
begin()
        
        
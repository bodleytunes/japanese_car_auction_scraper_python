from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.keys import Keys
import time

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
css_login_ok = "input.ajneo3"

def begin():
    #full screen
    
    #driver.find_element_by_tag_name("body").send_keys(Keys.F11)
    driver.get(scrape_url)
    #authenticate and login
    authenticate()
    # Choose vehicle
    # Create vehicles to search list
    vehicles_to_search.append(vehicle_to_search(vehicle_make, vehicle_model))
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
    driver.find_element_by_class_name("ajneo3").click()
    
def vehicle_stuff():
    
    for search_vehicle in vehicles_to_search:
        time.sleep(4)
        # Only continue to do the vehicle stuff if make or model is present! otherwise loop around to next vehicle in the list.  
        if(choose_make_link(search_vehicle.make)):
            time.sleep(4)
            if(choose_model(search_vehicle.model)):
                time.sleep(5)
                print("Model done!")          
#                page_count = count_pages()
#                row_count = count_rows()
#                get_rows(row_count, page_count)
                # Now click button to return to home screen (to select make)
                driver.find_element_by_class_name("aj_exp").click()        
            else:
                #if no model on page, then click home
                print("no model!")
                time.sleep(2)
                driver.find_element_by_class_name("nachalo").click()
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
    
    page_count = 0
    
    return page_count()

def row_count():
    
    row_count = 0
    
    return row_count

def next_page(page_number):
    click_page(page_number)
            
def get_row():
    row_data = xxxxxxxx
    return row_data

def get_rows(row_count, page_count):
    
    for p in range(page_count):
        for r in range(row_count):
            row_data = get_row(r)
            vehicles.append(vehicle(row_data))
        next_page(page_number)
        
        parse_vehicles(vehicles)

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
    
    def __init__(self, make=None,model=None,year=None,miles=None,grade=None,date=None,start_price=None,end_price=None):
        
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
        
        
    



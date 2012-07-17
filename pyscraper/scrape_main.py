from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

scrape_url = "http://www.jpcenter.ru"
 # Create instance of chrome driver.
driver = webdriver.Chrome()
login_user = "monkey5"
login_password = "password"
vehicle_make = "GM"
vehicle_model = "CHEVROLET ASTRO"
xpath_login_box = "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/span/table/tbody/tr/td/input[2]"
css_login_ok = "input.ajneo3"

def begin():
    
    driver.get(scrape_url)
    #authenticate and login
    authenticate()
    # Choose vehicle
   

def authenticate():
    # Click login
    driver.find_element_by_xpath(xpath_login_box).click()
    # Enter Username and password
    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys(login_user)
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys(login_password)
    #Click login
    driver.find_element_by_css_selector(css_login_ok).click()

def vehicle_stuff():
    
    for search_vehicle in vehicles_to_search:
        # Only continue to do the vehicle stuff if make or model is present! otherwise loop around to next vehicle in the list.
        if(choose_make()):
            if(choose_model()):
                page_count = count_pages()
                row_count = count_rows()
                get_rows(row_count, page_count)
        
## Loop starts here for each vehicle
 
def choose_make():
    try:
        driver.get_make()
        return true
    except:
        return None
        
def choose_model():
    try:
        driver.get_model()
        return true
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
    
begin()

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
        
        
    



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
  
  

def authenticate():
    # Click login
    login = driver.find_element_by_xpath(xpath_login_box).click()
    # Enter Username and password
    username_elem = driver.find_element_by_name("username").clear()
    username_elem = driver.find_element_by_name("username").send_keys(login_user)
    password_elem = driver.find_element_by_name("password").clear()
    password_elem = driver.find_element_by_name("password").send_keys(login_password)
    #Click login
   
    driver.implicitly_wait(5)

    login_elem = driver.find_element_by_class_name("ajneo3")
    #login_elem.submit()
    driver.implicitly_wait(5)



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
        
        
    



from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.keys import Keys
import time
from datetime import date, datetime
from datetime import timedelta
from parse import htmlparser
import sys

from dbstuff import model


from sqlalchemy import *
from sqlalchemy import create_engine    
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import func
from sqlalchemy import distinct
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, Integer, ForeignKey, String, DateTime, Boolean
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base


scrape_url = "http://www.jpcenter.ru" #Url to scrape
 # Create instance of chrome driver.
driver = webdriver.Chrome()
#driver = webdriver.Firefox()
login_user = "monkey5"
login_password = "bingo"
vehicles_to_search = []
xpath_login_box = "/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/span/table/tbody/tr/td/input[2]"
css_login_ok = "ajneo3"
# Filename to write data to
f = open('c:\AuctionScraper\searchlog.txt', 'w')



def begin():

    driver.get(scrape_url)
    
    authenticate()  #authenticate and login
    # Choose vehicle
    # Create vehicles to search list
    #vehicles_to_search.append(vehicle_to_search(vehicle_make, vehicle_model))
    ## TOYOTA HIACE ##
    vehicles_to_search.append(vehicle_to_search("GM", "CHEVROLET ASTRO"))
    vehicles_to_search.append(vehicle_to_search("GMC", "CHEVROLET ASTRO"))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "HIACE VAN"))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "HIACE"))
    ## AMERICAN ##
   
   
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "CHEVROLET ASTRO"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "ASTRO"))
    vehicles_to_search.append(vehicle_to_search("GM", "CHEVROLET CHEVYVAN"))
    vehicles_to_search.append(vehicle_to_search("GMC", "CHEVROLET CHEVYVAN"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "CHEVROLET CHEVYVAN"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "CHEVYVAN"))
    vehicles_to_search.append(vehicle_to_search("GM", "VANDURA"))
    vehicles_to_search.append(vehicle_to_search("GMC", "VANDURA"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "VANDURA"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "VANDURA"))
    vehicles_to_search.append(vehicle_to_search("GMC", "OTHER"))
    vehicles_to_search.append(vehicle_to_search("GM", "OTHER"))
    vehicles_to_search.append(vehicle_to_search("CHEVROLET", "OTHER"))
    vehicles_to_search.append(vehicle_to_search("FORD", "OTHER"))
    
    ## JAP ##
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "TOWN ACE TRUCK"))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "LITE ACE TRUCK"))
    vehicles_to_search.append(vehicle_to_search("ISUZU", "ELF TRUCK"))
    vehicles_to_search.append(vehicle_to_search("MAZDA", "BONGO FRIENDEE"))
    vehicles_to_search.append(vehicle_to_search("NISSAN", "CARAVAN"))
    vehicles_to_search.append(vehicle_to_search("MAZDA", "RX-7"))
    vehicles_to_search.append(vehicle_to_search("TOYOTA", "ARISTO"))
    vehicles_to_search.append(vehicle_to_search("ISUZU", "RODEO"))
    vehicles_to_search.append(vehicle_to_search("MITSUBISHI", "DELICA TRUCK"))
    vehicles_to_search.append(vehicle_to_search("SUBARU", "SAMBAR"))
    vehicles_to_search.append(vehicle_to_search("SUBARU", "DOMINGO"))
    
    # set the current search day and search session
    set_day_id_and_search_session()
       
    vehicle_stuff()
    #write_unique_auction_houses()
    
    finish()

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
        global make # set as globals
        global model
        make = search_vehicle.make
        model = search_vehicle.model
       
        if(choose_make_link(search_vehicle.make) and choose_model(search_vehicle.model)):
            time.sleep(3)     
            # do the page stuff (nav / scrape / parse)
            do_pages()
            # Now click button to return to home screen (to select make)
            driver.find_element_by_class_name("aj_exp").click()        
        else:
            # if no model on page, then click home
            print("no model!")
            time.sleep(2)
            driver.find_element_by_class_name("nachalo").click()  # Click home
            
        print("finished vehicle" + " " + search_vehicle.make + " " + search_vehicle.model)
        
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
    
def do_pages():
    
    while (check_next_arrow_exists() or check_left_arrow_exists() or page_two_not_exists()):   # Check that either the left or right nav arrow for pages exists
        elements = driver.find_elements_by_class_name("navi1") #get all page number elements
        elements_unique = []  #create empty list for unique page numbers
        for element in elements:
            elements_unique.append(int(element.text)) #add to the new list as integer so can be sorted
            
        elements_unique = sorted(set(elements_unique))  # set makes unique, sort sorts the order
          
        page_count_run = len(elements_unique)  # total number of items in the list
        # if not right arrow then add one to the page count run otherwise it ends one too early
        if (check_next_arrow_exists()):
            page_count_run = page_count_run - 1 # minus one to get rid of the end high number page
        elif(page_count_run == 1):
             page_count_run = 2   # this to stop bombing out on single page
             
            
          
        for i in range(1, page_count_run):
            # Get Rows Data!
            get_row_data()
            # Click next page number
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
def page_two_not_exists():
    try:
        driver.find_element_by_xpath("//*[@class='navi1'][text()='2']")
        return False
    except:
        return True
def get_row_data():
    # Find all aj elements(row elements) | also remember the not operator to ditch the header row aj_view00!    
    row_elements = driver.find_elements_by_xpath("//tr[contains(@id, 'aj_view')][not(contains(@id, 'aj_view00'))]")
    number_of_rows = len(row_elements)
    
    global make
    global model
    
    db = GetDB()
    
    for row_element in row_elements:
        row_html = driver.execute_script("return arguments[0].innerHTML", row_element)
        htmlparser.start_parse(row_element, row_html, f, \
                                     make, model, db, day_id, search_session_id)
    # final save to db
    #db.commit()
        

            

        
def GetDB():
    engine = create_engine('postgresql://postgres:postgres@jmcmongo:5432/test')
# create a configured "Session" class
    NewSession = sessionmaker(bind=engine)
# create a Session
    db = NewSession()
    return db
    
def set_day_id_and_search_session():
    global day_id
    global search_session_id
    
    db = GetDB()
    
    insert_new_search_session()
    
    # latest search day
    resultset = db.query(model.SearchDay.id).order_by(desc(model.SearchDay.id)).first()
    day_id = resultset.id
    # latest search session
    resultset = db.query(model.SearchSession.id).order_by(desc(model.SearchSession.id)).first()
    search_session_id = resultset.id

def insert_new_search_session():
     #Insert new search session
    newdate = datetime.now()
    #Round time to nearest day by getting rid of the unwanted shizzle
    #Dont round this any more as will do this for the day session
    #newdate = newdate.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    
    print(newdate)
    
    db = GetDB()
    ss = model.SearchSession()
    ss.searchDate = newdate
    db.add(ss)
    db.commit()
    #Select new search session

def insert_new_search_day():
    db = GetDB()
    
    day = datetime.now()
    # Round to nearest day
    day = newDay.replace(hour = 0, minute = 0, second = 0, microsecond = 0)
    
    #get day from date
    dayofWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    actualDay = dayofWeek[date.weekday(day)]
    
    
    latest_search_day = db.query(model.SearchDay).order_by(desc(model.SearchDay.id)).first()
    
    if(latest_search_day.date != day):
        
    
        sd = model.SearchDay()
        
        sd.date = day
        sd.actualDay = actualDay
        
        print(str(day))
       
        #raw_input("day is above")
        
        # This is the save to db bit, that will allow you to try and write but if it exists it wont
        # throw an exception.
        
        db.merge(sd)
        try:
            db.commit() 
            print("Inserted new search day")
        except exc.SQLAlchemyError:
            db.rollback()
            print("found dupes")
     
    
def finish():
        
    driver.quit()
    

class vehicle_to_search():
    def __init__(self, make=None, model=None):
        self.make=make
        self.model=model
        
begin()
        
        
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time

def begin():
    
    # Create instance of chrome driver.
    driver = webdriver.Chrome()
    driver.get("http://www.jpcenter.ru")
    #authenticate and login
    authenticate(driver)
    # Choose vehicle
   

def authenticate(driver):
    # Click login
    driver.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/table/tbody/tr/td/table/tbody/tr[2]/td/span/table/tbody/tr/td/input[2]").click()
    # Enter Username and password
    driver.find_element_by_name("username").clear()
    driver.find_element_by_name("username").send_keys("monkey5")
    driver.find_element_by_name("password").clear()
    driver.find_element_by_name("password").send_keys("bingo")
    #Click login
    driver.find_element_by_css_selector("input.ajneo3").click()
    
def finish():
    
    driver.quit()
    
begin()
    



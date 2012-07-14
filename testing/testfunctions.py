from datetime import date, datetime
from datetime import timedelta
import time


def print_date_completed():
    
    print "Successfull FULL Scrape @ " + str(time.time()) + " "  + str(date.today())
    

print_date_completed()
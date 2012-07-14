# This is app.py


from flask import Flask, render_template, request, flash, session, redirect, url_for
from auctionbase import *
from auctionbase import *
from sqlalchemy import *
from sqlalchemy import create_engine
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from datetime import *
from datetime import timedelta
from datetime import date




app = Flask(__name__)
app.debug = True

@app.route('/today', methods=['POST','GET'])
def Today():


    db = query.GetDB()
    
    today = datetime.now()
    dayToday= today.replace(hour=0,minute=0,second=0,microsecond=0)
    
    # Get list of searchvehicles for select box.    
    searchvehicles = db.query(model.Day2SearchVehicle)\
                   .join(model.Day2SearchVehicle.searchvehicle)\
                   .join(model.Day2SearchVehicle.day)\
                   .filter(model.SearchDay.date == dayToday)\
                   .all()

                   
    users = query.GetAllUsers()
    
    
    dayId = db.query(model.SearchDay).filter(model.SearchDay.date == dayToday).first()

    if request.method == 'POST':
        
        id = request.form.get('svselect')
        #day_id = request.form.get('sdselect') 
               
        
        return redirect(url_for('SearchBySearchVehicleId', searchvehicle_id=int(id), searchday_id=dayId.id))

          
        
    #return redirect(url_for('SearchBySearchVehicleId', searchvehicle_id=int(id)))
    
    
    return render_template('index2.html', searchvehicles=searchvehicles)

@app.route('/index', methods=['POST','GET'])
def Index():
    
    db = query.GetDB()
    
    # Get list of searchvehicles for select box.    
#    searchvehicles = db.query(model.VehicleStat)\
#                   .join(model.VehicleStat.SearchVehicle)\
#                   .all()
#                
    searchvehicles = db.query(model.SearchVehicle)\
                    .all()
                

    # Get search days for search day select box.
    searchdays = db.query(model.SearchDay).order_by(desc(model.SearchDay.date)).all()
    
    if request.method == 'POST':
        
        id = request.form.get('svselect')
        day_id = request.form.get('sdselect')        
        return redirect(url_for('SearchBySearchVehicleId', searchvehicle_id=int(id), searchday_id=day_id))
    
    
    return render_template('index.html', searchvehicles=searchvehicles, searchdays=searchdays)

@app.route('/searchfrom', methods=['POST','GET'])
def SearchFrom():
    
    db = query.GetDB()
    
    
    
    # Get list of searchvehicles for select box.    
    searchvehiclelist = db.query(model.SearchVehicle).all()
    # Get search days for search day select box.
    searchdays = db.query(model.SearchDay).order_by(desc(model.SearchDay.date)).all()
    
    if request.method == 'POST':
        
        id = request.form.get('svselect')
        day_id = request.form.get('sdselect')        
        
        return redirect(url_for('SearchFromDate', searchvehicle_id=int(id), searchday_id=day_id))
    
    
    return render_template('index.html', searchvehicles=searchvehiclelist, searchdays=searchdays)

@app.route('/searchfromdate/<searchvehicle_id>/<searchday_id>', methods=['POST','GET'])
def SearchFromDate(searchvehicle_id, searchday_id, methods=['POST','GET']):
    
    db = query.GetDB()
    db2 = query.GetDB()
    
    userlist = query.GetAllUsers()
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .join(model.AuctionVehicle.searchDay)\
            .join(model.AuctionVehicle.searchSession)\
            .filter(and_(model.AuctionVehicle.day_id >= searchday_id, model.SearchVehicle.id == searchvehicle_id))\
            .order_by(desc(model.AuctionVehicle.day_id))\
            .all()
            
    total =  db2.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .filter(and_(model.AuctionVehicle.day_id >= searchday_id, model.SearchVehicle.id == searchvehicle_id))\
            .count()
            
    if request.method == 'POST':
            interests = request.form.getlist('mark_interest')
            interestList = []
            interestVehicles = []
            user_id = request.form.get('userselect')
        
            for item in interests:
                flash("http://quadcore:5000/individual/" + str(item))
                interestList.append(item)
            
            for item in interests:
                interestVehicles.append(item)
            
            #send list of id's of selected vehicles to method to pull back new cursor
            
            interestedVehiclesCursor = query.InterestedVehicleOps(interestVehicles)
                
            query.FavouriteOps(interestedVehiclesCursor, user_id)
            
            todaysFavourites = query.GetAllFavouritesToday()
        
            
            #return render_template('vehicle.html', vehicles=todaysFavourites, total=total)
            return redirect(url_for('Favourites'))
            
       
    
    
    return render_template('vehicle.html', vehicles=cursor, total=total, userlist=userlist)

@app.route('/messages', methods=['POST','GET'])
def Messages(interestVehicles):
    return render_template('messages.html', interestVehicles)

@app.route('/searchvehicle/<searchvehicle_id>/<searchday_id>', methods=['POST','GET'])
def SearchBySearchVehicleId(searchvehicle_id, searchday_id):
    
    db = query.GetDB()
    db2 = query.GetDB()
    
    userlist = query.GetAllUsers()
    
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .join(model.AuctionVehicle.searchDay)\
            .join(model.AuctionVehicle.searchSession)\
            .filter(and_(model.AuctionVehicle.day_id == searchday_id, model.SearchVehicle.id == searchvehicle_id, model.AuctionVehicle.year < 2003))\
            .order_by(desc(model.AuctionVehicle.day_id))\
            .all()
            
    total =  db2.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .filter(and_(model.AuctionVehicle.day_id == searchday_id, model.SearchVehicle.id == searchvehicle_id))\
            .count()
            
    if request.method == 'POST':
            interests = request.form.getlist('mark_interest')
            interestList = []
            interestVehicles = []
            user_id = request.form.get('userselect')
        
            for item in interests:
                flash("http://quadcore:5000/individual/" + str(item))
                interestList.append(item)
            
            for item in interests:
                interestVehicles.append(item)
            
            #send list of id's of selected vehicles to method to pull back new cursor
            
            interestedVehiclesCursor = query.InterestedVehicleOps(interestVehicles)
                
            query.FavouriteOps(interestedVehiclesCursor, user_id)
            
            todaysFavourites = query.GetAllFavouritesToday()
        
            
            #return render_template('vehicle.html', vehicles=todaysFavourites, total=total)
            return redirect(url_for('Favourites'))
    
    
    
    return render_template('vehicle.html', vehicles=cursor, total=total, userlist=userlist)

@app.route('/favourites', methods=['POST','GET'])
def Favourites():
    
    cursor = query.GetAllFavouritesToday()
    
    return render_template('vehicle.html', vehicles=cursor)

@app.route('/favourites/all', methods=['POST','GET'])
def FavouritesAll():
    
    cursor = query.GetAllFavouritesAll()
    
    return render_template('vehicle.html', vehicles=cursor)
    
    
@app.route('/<searchsession>/<themodel>', methods=['POST','GET'])
def SearchSessionAndModelSearch(searchsession, themodel):
    
    db = query.GetDB()
    db2 = query.GetDB()
    
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .join(model.AuctionVehicle.searchDay)\
            .join(model.AuctionVehicle.searchSession)\
            .filter(model.AuctionVehicle.searchSession_id == searchsession)\
            .filter(model.SearchVehicle.model == themodel)\
            .all()
            
    total =  db2.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .filter(and_(model.AuctionVehicle.searchSession_id == searchsession, model.SearchVehicle.model == themodel))\
            .count()
            
    if request.method == 'POST':
        interests = request.form.getlist('mark_interest')
        
        for item in interests:
            flash(item)
        
        return redirect(url_for('Messages'))
        
       
    
    
    return render_template('vehicle.html', vehicles=cursor, total=total)

@app.route('/lot/<thelotnumber>', methods=['POST','GET'])
def LotSearch(thelotnumber):
    
    db = query.GetDB()
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .filter(model.AuctionVehicle.lotNumber == thelotnumber)\
            .all()
    
    return render_template('vehicle.html', vehicles=cursor, message="Searching by Auction LotNumber")


@app.route('/chassis/<thechassiscode>', methods=['POST','GET'])
def ChassisSearch(thechassiscode):
    
    db = query.GetDB()
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchVehicle)\
            .filter(model.AuctionVehicle.chassis == thechassiscode)\
            .all()
    
    return render_template('vehicle.html', vehicles=cursor, message="Searching by Auction LotNumber")

@app.route('/day/<whatday>')
def SearchToday(whatday):
    
    if whatday == "today":
       #todays date
       newDay = datetime.now()
       # trim todays date
       date = newDay.replace(hour=0,minute=0,second=0,microsecond=0)
    
    db = query.GetDB()
    
    cursor = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchDay)\
            .filter(model.SearchDay.date == date)\
            .all()
    
    count = db.query(model.AuctionVehicle)\
            .join(model.AuctionVehicle.searchDay)\
            .filter(model.SearchDay.date == date)\
            .count()  
            
    if request.method == 'POST':
        interests = request.form.getlist('mark_interest')
        
        for item in interests:
            flash(item)
        
        return redirect(url_for('Messages'))    
    
    
    return render_template('vehicle.html', vehicles=cursor, total=count, message="Searching by Auction day")

@app.route('/days/last/<numberOfDays>/<themodel>', methods=['POST','GET'])
def SearchLast7(numberOfDays, themodel):
    
    if int(numberOfDays) < 8:
       #todays date
        newDay = datetime.now()
    #   # trim todays date
        date = newDay.replace(hour=0,minute=0,second=0,microsecond=0)
       
        date = date - timedelta(days=int(numberOfDays))
    
        db = query.GetDB()
   
        cursor = db.query(model.AuctionVehicle)\
                .join(model.AuctionVehicle.searchDay)\
                .join(model.AuctionVehicle.searchVehicle)\
                .filter(and_(model.SearchVehicle.model == themodel, model.SearchDay.date >= date))\
                .order_by(desc(model.SearchDay.date))\
                .all()
        
        count = db.query(model.AuctionVehicle)\
                .join(model.AuctionVehicle.searchDay)\
                .join(model.AuctionVehicle.searchVehicle)\
                .filter(and_(model.SearchVehicle.model == themodel, model.SearchDay.date >= date))\
                .order_by(desc(model.SearchDay.date))\
                .count()
                
        if request.method == 'POST':
            interests = request.form.getlist('mark_interest')
        
            for item in interests:
                flash(item)
        
        return redirect(url_for('Messages'))       
    
                
    else:
        cursor = None
    
    return render_template('vehicle.html', vehicles=cursor, total=int(count), message="Searching by Auction day")

@app.route('/individual/<theId>', methods=['POST','GET'])
def Individual(theId):
    
       
    db = query.GetDB()
   
    cursor = db.query(model.AuctionVehicle)\
                .join(model.AuctionVehicle.searchVehicle)\
                .filter(model.AuctionVehicle.id == int(theId))\
                .first()
                
       
    
    
    return render_template('vehicleInd.html', vehicles=cursor, message="Searching by Auction day")

# set the secret key.  keep this really secret:
app.secret_key = 'AFJOIJF3898UJDF...FO[[AFIFjfd'

if __name__ == "__main__":
    app.run(host='0.0.0.0')




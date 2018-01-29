from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy.orm import sessionmaker
from database_setup import Category, Garage, Car_Item, User, Base, Owner_Messages
from sqlalchemy import create_engine, or_, and_

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from flask import make_response
import requests
import os

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']

engine = create_engine("sqlite:///car_catalog4.db")
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import session as login_session
import random, string

#UPLOAD_FOLDER = os.path.basename('uploads')
#app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#User Helper Functions

def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id

def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user

def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None


@app.route('/gconnect', methods=['POST'])
def gconnect():
    #Validate state token

    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Obtain authorization code
    code = request.data

    try:
        #Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)

    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s' % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # if there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is valid for the intended user
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    #Verify that the access token is valid for this app
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's"), 401)
        print "Token's client ID does not match app's"
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response


    #Store the access token in the session for later use
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    #Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    # Add provider to Login Session
    login_session['provider'] = 'google'

    # see if user exists. If it doesn't, make a new one

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px; border-radius: 150px; -webkit-border-radius: 150px; -moz-border-radius: 150px;">'
    flash('you are now logged in as %s' % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconnect')
def gdisconnect():
    # Only disconnect a connected user.
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % access_token
    h = httplib2.Http()
    result = h.request(url, "GET")[0]
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['provider']
        response = make_response(json.dumps("Successfully disconnected."), 200)
        response.headers['Content-Type'] = 'application/json'
        flash("You have been successfully looged out.")
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.'), 400)
        response.headers['Content-Type'] = 'application/json'
        return response

@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"

    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    del login_session['facebook_id']
    del login_session['username']
    del login_session['email']
    del login_session['picture']
    del login_session['user_id']
    del login_session['provider']
    return "you have been logged out"

@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
        elif login_session['provider'] == 'facebook': 
            fbdisconnect()
        return redirect('/category')
    else:
        flash("You were not logged in to begin with!")
        return redirect("/category")

#Jasonify functions

@app.route("/category/JSON")
def categoryJSON():
    allCategories = session.query(Category).all()

    return jsonify(Category = [category.serialize for category in allCategories])

@app.route("/garage/JSON")
def garageJSON():
    allGarages = session.query(Garage).all()

    return jsonify(Garage = [garage.serialize for garage in allGarages])

@app.route("/cars/JSON")
def carsJSON():
    allCars = session.query(Car_Item).all()

    return jsonify(Car_Item = [car.serialize for car in allCars])

@app.route("/category/<int:category_id>/car/<int:car_id>/JSON")
def carFromCategory(category_id, car_id):
    category = session.query(Category).filter_by(id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()

    return jsonify(Car_Item = car.serialize)


@app.route("/garage/<int:garage_id>/car/<int:car_id>/JSON")
def carFromGarage(garage_id, car_id):
    garage = session.query(Garage).filter_by(id=garage_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()

    return jsonify(Car_Item=car.serialize)

@app.route("/messages/car/<int:car_id>/user/<int:user_id>JSON")
def owner_messages(car_id, user_id):
    user = session.query(User).filter_by(id=user_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    messages = session.query(Owner_Messages).filter_by(user_id=user_id).all()

    return jsonify(Owner_Messages= [message.serialize for message in messages])




@app.route("/login")
def showLogin():
    state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
    login_session["state"] = state
    #return "The current session state is %s" % login_session['state']
    return render_template("login.html", STATE=state)




@app.route('/')
@app.route('/category')
def category():
    categories = session.query(Category).all()
    garages = session.query(Garage).all()

    if 'username' not in login_session:
        return render_template('public_index.html', categories=categories, garages=garages)
    else:

        return render_template("index.html", categories=categories, garages=garages)

# Category related Functions
@app.route('/category/<int:category_id>')
def category_items(category_id):
    category = session.query(Category).filter_by(id=category_id).one()
    cars = session.query(Car_Item).filter_by(category_id=category.id).all()
    #creator = getUserInfo(category.user_id)

    if 'username' not in login_session:
        return render_template('public_category_items.html', category=category, cars=cars)
    else:

        return render_template("category_items.html", category=category, cars=cars)

@app.route('/category/<int:category_id>/cars/<int:car_id>')
def car_from_category(category_id, car_id):
    category = session.query(Category).filter_by(id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    creator = getUserInfo(car.user_id)

    if "username" not in login_session:
        return render_template("public_car_in_category.html", category=category, car=car)
    elif "username" in login_session and creator.id != login_session["user_id"]:
        return render_template("car_in_category_not_owner.html", category=category, car=car)
    else: 
        return render_template("car_in_category_owner.html", category=category, car=car)


@app.route('/category/<int:category_id>/cars/<int:car_id>/purchase', methods=["POST", "GET"])
def purchase_from_category(category_id, car_id):
    category = session.query(Category).filter_by(id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()
    
    if "username" not in login_session:
        return redirect('/login') 
    else:
        if request.method == "POST":
            message = Owner_Messages(buyer_name=request.form['name'], buyer_email=request.form['email'], buyer_phone=request.form['bid'], buyer_message=request.form['mymessage'], car_id=car.id, user_id=user.id)
            session.add(message)
            session.commit()
            return render_template('purchase_confirm.html', category=category, car=car)
        else:
            return render_template('category_purchase.html', category=category, car=car, user=user)

@app.route('/category/<int:category_id>/cars/<int:car_id>/confirm')
def category_purchase_confirm(category_id, car_id):
    category = session.query(Category).filter_by(id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()

    return render_template('purchase_confirm.html', category=category)

# Create a Car within a Category


@app.route('/category/<int:category_id>/create', methods=["POST", "GET"])
def create_car_for_category(category_id):

    category = session.query(Category).filter_by(id=category_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if request.method == "POST":
        if 'username' in login_session:
            newCar = Car_Item(make=request.form["make"],model=request.form["model"], year=request.form["year"], color=request.form["color"], price=request.form["price"], description=request.form["description"], milage=request.form["milage"], category_id=request.form["category"], user_id=login_session["user_id"])
            session.add(newCar)
            session.commit()
            flash("Congratulations, you have successfully entered a new vehicle to sell!")
            return redirect(url_for("category_items.html", category=category, cars=cars))
        else:
            return redirect('/login')
    else:
        return render_template('create_car_for_category.html', category=category)

# Edit a Car within a Category


@app.route('/category/<int:category_id>/cars/<int:car_id>/edit', methods=["POST", "GET"])
def edit_car_from_category(category_id, car_id):

    category = session.query(Category).filter_by(category_id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if user.id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not allowed to edit this vehicle. Please enter your own vehicle to sell first!')}</script>body onload='myFunction()'>"

    if request.method == "POST":

        if request.form['year']:
            car.year = request.form['year']
        if request.form['make']:
            car.year = request.form['make']
        if request.form['model']:
            car.year = request.form['model']
        if request.form['milage']:
            car.year = request.form['milage']
        if request.form['color']:
            car.year = request.form['color']
        if request.form['price']:
            car.year = request.form['price']
        if request.form['description']:
            car.year = request.form['description']
        if request.form['category']:
            car.year = request.form['category']
        session.add(car)
        session.commit()
        return redirect(url_for('car_in_category', category_id=category.id, car_id=car.id))
    else:

        return render_template('edit_car_from_category.html', category=category, car=car, user=user)

# Delete a Car within a Category


@app.route('/category/<int:category_id>/cars/<int:car_id>/delete', methods=["POST", "GET"])
def delete_car_from_category(category_id, car_id):

    category = session.query(Category).filter_by(category_id=category_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if user.id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not allowed to delete this vehicle. You can only delete vehicles you have entered yourself!')}</script>body onload='myFunction()'>"

    if request.method == "POST":
        session.delete(car)
        session.commit()
        flash('Vehicle successfully Deleted!')
        return redirect(url_for('category_items', category_id=category.id))
    else:
        return render_template('delete_car_from_category.html', category=category, car=car, user=user)


# Garage related Functions

@app.route('/garage/<int:garage_id>')
def garage_items(garage_id):
    garage = session.query(Garage).filter_by(id=garage_id).one()
    cars = session.query(Car_Item).filter_by(garage_id=garage.id).all()
    user = session.query(User).filter_by(id=garage.user_id).one()
    creator = getUserInfo(garage.user_id)

    if 'username' not in login_session:
        return render_template('public_garage_items.html', garage=garage, cars=cars, user=user)
    elif 'username' in login_session and creator.id != login_session["user_id"]:
        return render_template('garage_items_not_owner.html', garage=garage, cars=cars, user=user)
    else:
        return render_template("garage_items_owner.html", garage=garage, cars=cars, user=user)


@app.route('/garage/<int:garage_id>/cars/<int:car_id>')
def car_from_garage(garage_id, car_id):
    garage = session.query(Garage).filter_by(id=garage_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()
    creator = getUserInfo(car.user_id)

    if "username" not in login_session:
        return render_template("public_car_in_garage.html", garage=garage, car=car)
    elif "username" in login_session and creator.id != login_session["user_id"]:
        return render_template("car_in_garage_not_owner.html", garage=garage, car=car)
    else: 
        return render_template("car_in_garage_owner.html", garage=garage, car=car, user=user)

@app.route('/garage/<int:garage_id>/cars/<int:car_id>/purchase', methods=["POST", "GET"])
def purchase_from_garage(garage_id, car_id):
    garage = session.query(Garage).filter_by(id=garage_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == "POST":
            return render_template("purchase_confirm.html", garage=garage, car=car)
        else:	
            return render_template('garage_purchase.html', garage=garage, car=car, user=user)


@app.route('/confirm/<int:garage_id>')
def garage_purchase_confirm(garage_id):
    garage = session.query(Garage).filter_by(id=garage_id).one()

    return render_template('purchase_confirm.html', garage=garage)


# Create a Car within a Garage


@app.route('/garage/<int:garage_id>/create', methods=["POST", "GET"])
def create_car_for_garage(garage_id):

    garage = session.query(Garage).filter_by(id=garage_id).one()


    if 'username' not in login_session:
        return redirect('/login')

    

    if request.method == "POST":

        newCar = Car_Item(make= request.form["make"], model=request.form["model"], year=request.form["year"], color=request.form["color"], price=request.form["price"], description=request.form["description"], milage=request.form["milage"], category_id= request.form['category'], user_id=garage.user_id, garage_id=garage.id)
        session.add(newCar)
        session.commit()
        return redirect(url_for("garage_items", garage_id=garage.id))
    else:

        return render_template('create_car_for_garage.html', garage=garage)


# Edit Car within a Garage

@app.route('/garage/<int:garage_id>/cars/<int:car_id>/edit', methods=["POST", "GET"])
def edit_car_from_garage(garage_id, car_id):

    garage = session.query(Garage).filter_by(id=garage_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if user.id != login_session['user_id']:
        return "<script>function myFunction(){alert('You are not allowed to edit this vehicle. Please enter your own vehicle to sell first!')}</script>body onload='myFunction()'>"

    if request.method == "POST":

        if request.form['year']:
            car.year = request.form['year']
        if request.form['make']:
            car.year = request.form['make']
        if request.form['model']:
            car.year = request.form['model']
        if request.form['milage']:
            car.year = request.form['milage']
        if request.form['color']:
            car.year = request.form['color']
        if request.form['price']:
            car.year = request.form['price']
        if request.form['description']:
            car.year = request.form['description']
        if request.form['category']:
            car.year = request.form['category']
        session.add(car)
        session.commit()
        return redirect(url_for('car_in_garage', garage_id=garage.id, car_id=car.id))
    else:

        return render_template('edit_car_from_garage.html', garage=garage, car=car, user=user)


# Delete a Car within a Garage


@app.route('/garage/<int:garage_id>/cars/<int:car_id>/delete', methods=["POST", "GET"])
def delete_car_from_garage(garage_id, car_id):

    garage = session.query(Garage).filter_by(id=garage_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    user = session.query(User).filter_by(id=car.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if user.id != login_session['user_id']:
        return "<script>function myFunction(){alert('If you are not the owner of this vehicle, you are not allowed to delete it!')}</script>body onload='myFunction()'>"

    if request.method == "POST":
        session.delete(car)
        session.commit()
        flash('Vehicle successfully Deleted!')
        return redirect(url_for('category_items', category_id=category.id))
    else:

        return render_template('delete_car_from_garage.html', garage=garage, car=car, user=user)

# Create a Garage
@app.route('/garage/new', methods=["POST", "GET"])
def create_garage():

    if 'username' not in login_session:
        return redirect('/login')
    else:
        if request.method == "POST":

            newGarage = Garage(name = request.form["name"], garage_description= request.form["description"], user_id = login_session['user_id'])
            session.add(newGarage)
            session.commit()
            return redirect(url_for("category"))
        else:
            return render_template("create_garage.html")

@app.route('/garage/<int:garage_id>/delete', methods=["POST", "GET"])
def delete_garage(garage_id):

    garage = session.query(Garage).filter_by(id=garage_id).one()
    cars = session.query(Car_Item).filter_by(garage_id=garage.id).all()
    user = session.query(User).filter_by(id=garage.user_id).one()

    if 'username' not in login_session:
        return redirect('/login')

    if user.id != login_session['user_id']:
        return "<script>function myFunction(){alert('If you are not the owner of this garage, you are not allowed to delete it!')}</script>body onload='myFunction()'>"

    if request.method == "POST":

        for car in cars:
            session.delete(car)
            session.commit()

        session.delete(garage)
        session.commit()
        flash('Garage successfully Deleted!')
        return redirect(url_for('category'))

    else:

        return render_template('delete_garage.html', garage=garage, car=car, user=user)

@app.route('/user/<int:user_id>/car/<int:car_id>/messages/')
def messages_to_owner(user_id, car_id):
    user = session.query(User).filter_by(id=user_id).one()
    car = session.query(Car_Item).filter_by(id=car_id).one()
    bids = session.query(Owner_Messages).filter_by(car_id=car.id).all()

    if 'username' not in login_session or user.id != login_session['user_id']:
        return redirect('/login')
    else:
        return render_template('owner_messages.html', bids=bids, user=user, car=car)







if __name__ == '__main__':
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host = '0.0.0.0', port = 5000)
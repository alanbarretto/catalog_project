from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy.orm import sessionmaker
from database_setup import Category, Garage, Car_Item, User, Base
from sqlalchemy import create_engine, or_, and_

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from flask import make_response
import requests

#CLIENT_ID = json.loads(
#	open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine("sqlite:///car_catalog3.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import session as login_session
import random, string

#User Helper Functions

def createUser(login_session):
	newUser = User(name=login_session['username'], email=login_session['email'], picture=login_session['picture'])
	session.add(newUser)
	session.commit()
	user = session.query(User).filter_by(email=login_session['email']).one()
	return user.id

def getUserInfo(user_id):
	user= session.query(User).filter_by(id=user_id).one()
	return userinfo_url

def getUserID(email):
	try:
		user = session.query(User).filter_by(email=email).one()
		return user.id
	except:
		return None





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



@app.route("/login")
def showLogin():
	state = "".join(random.choice(string.ascii_uppercase + string.digits) for x in xrange(32))
	login_session["state"] = state

	return render_template("login.html", STATE=state)




@app.route('/')
@app.route('/category')
def category():
	categories = session.query(Category).all()
	garages = session.query(Garage).all()

	if 'username' not in login_session:
		return render_template('publichomepage.html', categories=categories, garages=garages)
	else:

		return render_template("homepage.html", categories=categories, garages=garages)




# Category related Functions

@app.route('/category/<int:category_id>')
def category_items(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	
	cars = session.query(Car_Item).filter_by(category_id = category.id).all()

	#creator = getUserInfo(category.user_id)

	if 'username' not in login_session:
		return render_template('public_category_items.html', categories=categories, cars=cars)
	else:
	
		return render_template("category_items.html", category=category, cars=cars)








@app.route('/category/<int:category_id>/cars/<int:car_id>')
def specific_car_category(category_id, car_id):
	category = session.query(Category).filter_by(id=category_id).one()
	car = session.query(Car_Item).filter_by(id= car_id).one()
	creator = getUserInfo(car.user_id)

	if "username" not in login_session or creator.id != login_session["user_id"]:
    	return render_template("public_specific_car_category.html", category=category, car=car)
    else:
		return render_template("specific_car_category.html", category=category, car=car)


@app.route('/category/<int:category_id>/cars/<int:car_id>/purchase', methods=["post", "get"])
def purchase_from_category(category_id, car_id):
	category = session.query(Category).filter_by(id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()

	if 'username' not in login_session:
		return render_template('public_category_purchase.html', categories=categories, car=car, user=user)
	else:
		return render_template('category_purchase.html', category=category, car=car, user=user)

@app.route('/confirm/<int:category_id>')
def category_purchase_confirm(category_id, car_id):
	category = session.query(Category).filter_by(id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()

	

	return render_template('category_purchase_confirm.html', category=category)

# Create a Car within a Category


@app.route('/category/<int:category_id>/create', methods=["post", "get"])
def create_car_category(category_id):

	category = session.query(Category).filter_by(id=category_id).one()
	cars = session.query(Car_Item).filter_by(category_id=category.id).all()

	if 'username' not in login_session:
		return redirect('/login')

	if request.method == "post":

		newCar = Car_Item(make= request.form["make"], model=request.form["model"], year=request.form["year"], \
					color=request.form["color"], price=request.form["price"], description=request.form["description"], \
					milage=request.form["milage"], car_item_pic=request.form["car_pic"], user_id=login_session["user_id"])
		session.add(newCar)
		session.commit()
		flash("Congratulations, you have successfully entered a new vehicle to sell!")
		return redirect(url_for("category_items.html", category=category, cars=cars))

	return render_template('newCarCategory.html', category=category)

# Edit a Car within a Category

@app.route('/category/<int:category_id>/cars/<int:car_id>/edit')
def edit_car_category(category_id, car_id):

	category = session.query(Category).filter_by(category_id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()




	return render_template('editCarCategory.html', category=category, car=car, user=user)

# Delete a Car within a Category

@app.route('/category/<int:category_id>/cars/<int:car_id>/delete')
def delete_car_category(category_id, car_id):

	category = session.query(Category).filter_by(category_id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()


	return render_template('deleteCarCategory.html', category=category, car=car, user=user)


# Garage related Functions

@app.route('/garage/<int:garage_id>')
def garage_items(garage_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()
	cars = session.query(Car_Item).filter_by(garage_id=garage.id).all()
	user = session.query(User).filter_by(id=garage.user_id).one()
	creator = getUserInfo(car.user_id)

	if 'username' not in login_session or creator.id != login_session["user_id"]:
		return render_template('public_garage_items.html', garage=garage, cars=cars, user=user)
	else:
		return render_template("garage_items.html", garage=garage, cars=cars, user=user)



@app.route('/garage/<int:garage_id>/cars/<int:car_id>')
def specific_car_garage(garage_id, car_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()
	car = session.query(Car_Item).filter_by(id = car_id).one()
	creator = getUserInfo(car.user_id)

	if "username" not in login_session or creator.id != login_session["user_id"]:
    	return render_template("public_specific_car_garage.html", garage=garage, car=car)
    else:
		return render_template("specific_car_garage.html", garage=garage, car=car)



@app.route('/garage/<int:garage_id>/cars/<int:car_id>/purchase', methods=["post", "get"])
def purchase_from_garage(garage_id, car_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()

	if "username" not in login_session:
		return render_template("public_garage_purchase.html", garage=garage, car=car, user=user)
	else:	
		return render_template('garage_purchase.html', garage=garage, car=car, user=user)


@app.route('/confirm/<int:garage_id>')
def garage_purchase_confirm(garage_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()

	return render_template('garage_purchase_confirm.html', garage=garage)


# Create a Car within a Garage


@app.route('/category/<int:garage_id>/create', methods=["post", "get"])
def create_car_garage(garage_id):

	garage = session.query(Garage).filter_by(id=garage_id).one()


	return render_template('newCarGarage.html', garage=garage)


# Edit Car within a Garage

@app.route('/garage/<int:garage_id>/cars/<int:car_id>/edit', methods=["post", "get"])
def edit_car_garage(garage_id, car_id):

	garage = session.query(Garage).filter_by(id=garage_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()



	return render_template('editCarGarage.html', garage=garage, car=car, user=user)


# Delete a Car within a Garage


@app.route('/garage/<int:garage_id>/cars/<int:car_id>/delete', methods=["post", "get"])
def delete_car_garage(garage_id, car_id):

	garage = session.query(Garage).filter_by(id=garage_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()


	return render_template('deleteCarGarage.html', garage=garage, car=car, user=user)

# Create a Garage
@app.route('/garage/new', methods=["Post", "Get"])
def create_garage():

	if request.method== "Post":

		newGarage = Garage(name = request.form["name"], garage_description= request.form["description"], \
			user_id = login_session['user_id'])
		session.add(newGarage)
		session.commit()
		return redirect(url_for("catalog"))
	else:
		return render_template("create_garage.html")



if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
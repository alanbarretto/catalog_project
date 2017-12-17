from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy.orm import sessionmaker
from database_setup import Category, Car_Item, User, Base
from sqlalchemy import create_engine

from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json

from flask import make_response
import requests

#CLIENT_ID = json.loads(
#	open('client_secrets.json', 'r').read())['web']['client_id']

engine = create_engine("sqlite:///car_catalog.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

from flask import session as login_session
import random, string





@app.route('/')
@app.route('/category')
def category():
	category = session.query(Category).all()
	garages = session.query(Garage).all()


	return render_template("homepage.html", category=category, garages=garages)






@app.route('/category/<int:category_id>')
def category_items(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	cars = session.query(Car_Item).filter_by(category_id = category.id).all()
	#creator = getUserInfo(category.user_id)

	
	return render_template("category_items.html", category=category, cars=cars)








@app.route('/category/<int:category_id>/cars/<int:car_id>')
def specific_car(category_id, car_id):
	category = session.query(Category).filter_by(id=category_id).one()
	car = session.query(Car_Item).filter_by(id = car_id).one()



	return render_template("specific_car.html", category=category, car=car)


@app.route('category/<int:category_id>/cars/<int:car_id>/purchase', methods="post", "get")
def purchase_from_category(category_id, car_id):
	category = session.query(Category).filter_by(id=category_id).one()
	car = session.query(Car_Item).filter_by(category_id=category.id, id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()

	return render_template('purchase.html', category=category, car=car, user=user)




@app.route('garage/<int:garage_id>/cars/<int:car_id>/purchase', methods="post", "get")
def purchase_from_garage(garage_id, car_id):
	category = session.query(Garage).filter_by(id=garage_id).one()
	car = session.query(Car_Item).filter_by(garage_id=garage_id, id=car_id).one()
	user = session.query(User).filter_by(id=car.user_id).one()

	return render_template('purchase.html', category=category, car=car, user=user)





@app.route('/confirm/<int:category_id>')
def category_purchase_confirm(category_id):
	category = session.query(Category).filter_by(id=category_id).one()

	return render_template('category_purchase_confirm.html', category=category)




@app.route('/confirm/<int:garage_id>')
def garage_purchase_confirm(garage_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()

	return render_template('garage_purchase_confirm.html', garage=garage)



@app.route('/garage/<int:garage_id>')
def garage_items(garage_id):
	garage = session.query(Garage).filter_by(id=garage_id).one()
	cars = session.query(Car_Item).filter_by(garage_id=garage.id).all()
	user = session.query(User).filter_by(id=garage.user_id).one()


	return render_template("garage.html", garage=garage, cars=cars, user=user)






@app.route('/garage/create')
def create_garage():
	return "Create category here"







@app.route('/category/<int:category_id>/edit', methods="post", "get")
def edit_category(category_id):

	category = session.query(Category).filter_by(category_id=category_id).one()


	return render_template('editCategory.html', category=category)







@app.route('/category/<int:category_id>/delete', methods="post", "get")
def delete_category(category_id):
	category = session.query(Category).filter_by()




	return "Delete category here"








@app.route('/category/<intcategory_id>/create')
def create_car(category_id):

	category = session.query(Category).filter_by(category_id=category_id).one()


	return render_template('createCategory.html', category=category)








@app.route('/category/<int:category_id>/cars/<int:car_id>/edit')
def edit_car_category(category_id,car_id):

	category = session.query(Category).filter_by(category_id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()



	return render_template('editCar.html', category=category, car=car)





@app.route('/category/<intcategory_id>/cars/<int:car_id>/delete')
def delete_car_category(category_id, car_id):

	category = session.query(Category).filter_by(category_id=category_id).one()
	car = session.query(Car_Item).filter_by(id=car_id).one()


	return render_template('deleteCar.html', category=category, car=car)




if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
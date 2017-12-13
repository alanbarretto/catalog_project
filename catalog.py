from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from sqlalchemy.orm import sessionmaker
from database_setup import Bodystyle, Car_Item, User, Base
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


	return render_template("homepage.html", category=category)

@app.route('/category/<int:category_id>/cars')
def cars_by_make_model(category_id):
	category = session.query(Category).filter_by(id=category_id).one()
	carItem = session.query(Car_Item).filter_by(category_id = category.id).all()
	#creator = getUserInfo(bodystyle.user_id)

	
	return render_template("catalog_items.html", category=category, carItem=carItem)

@app.route('/category/<int:category_id>/cars/<int:car_id>')
def specific_car(category_id, car_id):
	return render_template("specific_car.html")

@app.route('/category/create')
def create_category():
	return "Create category here"

@app.route('/category/<int:category_id>/edit', methods="post", "get")
def edit_category(category)
	return "Edit category here"

@app.route('/category/<int:category_id>/delete', methods="post", "get")
def delete_category(category_id):
	return "Delete category here"





@app.route('/category/<intcategory_id>/cars/create')
def create_carcategory_id):
	return "This page is for creating a new item"

@app.route('/category/<intcategory_id>/cars/<int:car_id>/edit')
def edit_car(category_id,car_id):
	return "This is where you can edit an item"

@app.route('/category/<intcategory_id>/cars/<int:car_id>/delete')
def delete_carcategory_id, car_id):
	return "You can delete an item here"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
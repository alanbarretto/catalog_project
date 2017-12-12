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
@app.route('/cars')
def cars_bodystyles():
	bodystyles = session.query(Bodystyle).all()


	return render_template("homepage.html", bodystyles=bodystyles)

@app.route('/catalog/<int:bodystyle_id>/items')
def cars_by_make_model(bodystyle_id):
	bodystyle = session.query(Bodystyle).filter_by(id=bodystyle_id).one()
	carItem = session.query(Car_Item).filter_by(bodystyle_id = bodystyle.id).all()
	#creator = getUserInfo(bodystyle.user_id)

	
	return render_template("catalog_items.html", bodystyle=bodystyle, carItem=carItem)

@app.route('/catalog/<int:bodystyle_id>/items/<int:car_id>')
def specific_car(bodystyle_id, car_id):
	return render_template("specific_car.html")



@app.route('/catalog/<int:catalog_id>/items/create')
def create_car(catalog_id):
	return "This page is for creating a new item"

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit')
def edit_car(catalog_id, item_id):
	return "This is where you can edit an item"

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete')
def delete_car(catalog_id, item_id):
	return "You can delete an item here"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
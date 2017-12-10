from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

car_catalog = [{"bodystyle": "SUV", "id": "1"}, {"bodystyle": "Luxury Cars", "id": "2"}, {"bodystyle": "Sedans", "id": "3"}, {"bodystyle": "Hybrids", "id": "4"}, {"bodystyle": "Sports Cars", "id": "5"}, {"bodystyle": "Pick Up Trucks", "id": "6"}]
individual_car = [{"bodystyle": "Hybrids", "make":"Toyota", "model":"Prius", "color":"blue", "year": "2010", "milage":"100000", "id": "4"}, {"bodystyle": "Hybrids", "make":"Toyota", "model":"Prius", "color":"red", "year": "2011", "milage":"110000", "id": "4"}, {"bodystyle": "SUV", "make":"Jeep", "model":"Compass", "color":"black", "year": "2017", "milage":"2894", "id": "1"}]



@app.route('/')
@app.route('/catalog')
def catalogHome():
	return render_template("homepage.html", car_catalog=car_catalog)

@app.route('/catalog/<int:bodystyle_id>/items')
def catalogItems(bodystyle_id):
	index = bodystyle_id - 1
	return render_template("catalog_items.html", individual_car=individual_car, bodystyle=car_catalog[index]['bodystyle'])

@app.route('/catalog/<int:bodystyle_id>/items/<int:car_id>')
def specificItem(bodystyle_id, car_id):
	return renter_template("specific_car.html")

@app.route('/catalog/create')
def createCatalog():
	return "This is the page where you are able to create a new catalog category"

@app.route('/catalog/<int:catalog_id>/edit')
def editCatalog(catalog_id):
	return "This is where you can edit a category"

@app.route('/catalog/<int:catalog_id>/delete')
def deleteCatalog(catalog_id):
	return "This is where you delete a category"

@app.route('/catalog/<int:catalog_id>/items/create')
def createItem(catalog_id):
	return "This page is for creating a new item"

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/edit')
def editItem(catalog_id, item_id):
	return "This is where you can edit an item"

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>/delete')
def deleteItem(catalog_id, item_id):
	return "You can delete an item here"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
from flask import Flask, render_template, request, redirect, url_for, flask, jsonify
app = Flask(__name__)

@app.route('/')
@app.route('/catalog')
def catalogHome():
	print "This is the home page"

@app.route('/catalog/<int:catalog_id/items')
def catalogItems():
	print "This is the page where the specific catalog displays with all the items under it"

@app.route('/catalog/<int:catalog_id>/items/<int:item_id>')
def specificItem():
	print "This is the page of a specific item under a category"

@app.route('/catalog/create')
def createCatalog():
	print "This is the page where you are able to create a new catalog category"

@app.route('/catalog/<int:catalog_id/edit')
def editCatalog():
	print "This is where you can edit a category"

@app.route('/catalog/<int:catalog_id/delete')
def deleteCatalog():
	print "This is where you delete a category"

@app.route('/catalog/<int:catalog_id/items/create')
def createItem():
	print "This page is for creating a new item"

@app.route('/catalog/<int:catalog_id/items/<int:item_id/edit')
def editItem():
	print "This is where you can edit an item"

@app.route('/catalog/<int:catalog_id/items/<int:item_id/delete')
def deleteItem():
	print "You can delete an item here"


if __name__ == '__main__':
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
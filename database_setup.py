import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String(140), nullable=False)
	email = Column(String(250), nullable=False)
	picture = Column(String(250))

class Category(Base):
	__tablename__ = 'category'

	id = Column(Integer, primary_key=True)
	category = Column(String(140), nullable=False)
	category_pic = Column(String(250))

class Garage(Base):
	__tablename__ = 'garage'

	id = Column(Integer, primary_key=True)
	name = Column(String(250), nullable=False)
	garage_pic = Column(String(250))
	garage_description = (Column(String(250)))
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)

class Car_Item(Base):
	__tablename__ = 'car_item'

	id = Column(Integer, primary_key=True)
	make = Column(String(140), nullable=False)
	model = Column(String(140), nullable=False)
	color= Column(String(140))
	year = Column(String(140), nullable=False)
	price = Column(String(140), nullable=False)
	description = Column(String(250))
	milage = Column(String(140), nullable=False)
	car_item_pic = Column(String(250))
	category_id = Column(Integer, ForeignKey('category.id'))
	category = relationship(Category)
	user_id = Column(Integer, ForeignKey('user.id'))
	user = relationship(User)
	garage_id = Column(Integer, ForeignKey('garage.id'))
	garage = relationship(Garage)



@property
def serialize(self):

	return {
		"make": self.make,
		"model": self.model,
		"id": self.id,
		"color": self.color,
		"year": self.year,
		"price": self.price,
		"description": self.description,
		"milage": self.milage,
		"car_item_pic": self.car_item_pic,
		"name": self.name,
		"garage_pic": self.garage_pic,
		"garage_description": self.garage_description,
		"email": self.email,
		"picture": self.picture,
		"category_pic": self.category_pic


	}

engine = create_engine('sqlite:///car_catalog3.db')
Base.metadata.create_all(engine)

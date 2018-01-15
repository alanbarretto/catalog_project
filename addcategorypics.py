from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Category, Base, Garage, Car_Item, User

engine = create_engine('sqlite:///car_catalog3.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()

category1 = session.query(Category).filter_by(id=1).one()

category1.category_pic = "static/uploads/sedan.jpg"

session.add(category1)
session.commit()

category2 = session.query(Category).filter_by(id=2).one()

category2.category_pic = "static/uploads/coupe.jpg"

session.add(category1)
session.commit()

category3 = session.query(Category).filter_by(id=3).one()

category3.category_pic = "static/uploads/suv.jpg"

session.add(category3)
session.commit()

category4 = session.query(Category).filter_by(id=4).one()

category4.category_pic = "static/uploads/crossover.jpg"

session.add(category4)
session.commit()

category5 = session.query(Category).filter_by(id=5).one()

category5.category_pic = "static/uploads/wagon.jpg"

session.add(category5)
session.commit()

category6 = session.query(Category).filter_by(id=6).one()

category6.category_pic = "static/uploads/hybrid.jpg"

session.add(category6)
session.commit()

category7 = session.query(Category).filter_by(id=7).one()

category7.category_pic = "static/uploads/convertible.jpg"

session.add(category7)
session.commit()

category8 = session.query(Category).filter_by(id=8).one()

category8.category_pic = "static/uploads/luxury.jpg"

session.add(category8)
session.commit()

category9 = session.query(Category).filter_by(id=9).one()

category9.category_pic = "static/uploads/sports.jpg"

session.add(category9)
session.commit()

category10 = session.query(Category).filter_by(id=10).one()

category10.category_pic = "static/uploads/pickup.jpg"

session.add(category10)
session.commit()

category11 = session.query(Category).filter_by(id=11).one()

category11.category_pic = "static/uploads/minivan.jpg"

session.add(category11)
session.commit()


print "all pics added!"
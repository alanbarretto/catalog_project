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

car1 = session.query(Car_Item).filter_by(id=1).one()

car1.car_item_pic = "static/uploads/toyotapriusblue.jpg"

session.add(car1)
session.commit()

car2 = session.query(Car_Item).filter_by(id=2).one()

car2.car_item_pic = "static/uploads/toyota_prius_2015_orange2.jpg"

session.add(car2)
session.commit()
car3 = session.query(Car_Item).filter_by(id=3).one()
car3.car_item_pic = "static/uploads/acura_tlx_2018_red2.jpg"

session.add(car3)
session.commit()

car4 = session.query(Car_Item).filter_by(id=4).one()

car4.car_item_pic = "static/uploads/Audi_A3_2018_yellow.jpg"

session.add(car4)
session.commit()


car5 = session.query(Car_Item).filter_by(id=5).one()

car5.car_item_pic = "static/uploads/ford_fusion_black2.jpg"

session.add(car5)
session.commit()

car6 = session.query(Car_Item).filter_by(id=6).one()

car6.car_item_pic = "static/uploads/bmw_m2_teal.jpg"

session.add(car6)
session.commit()

car7 = session.query(Car_Item).filter_by(id=7).one()

car7.car_item_pic = "static/uploads/jeep_compass_white.jpg"

session.add(car7)
session.commit()

car8 = session.query(Car_Item).filter_by(id=8).one()

car8.car_item_pic = "static/uploads/ford_explorer_red.jpeg"

session.add(car8)
session.commit()

car9 = session.query(Car_Item).filter_by(id=9).one()

car9.car_item_pic = "static/uploads/nissan_pathfinder_green.jpg"

session.add(car9)
session.commit()

car10 = session.query(Car_Item).filter_by(id=10).one()

car10.car_item_pic = "static/uploads/chevy_traverse_orange.jpg"

session.add(car10)
session.commit()

car11 = session.query(Car_Item).filter_by(id=11).one()

car11.car_item_pic = "static/uploads/kia_niro_red.jpg"

session.add(car11)
session.commit()

car12 = session.query(Car_Item).filter_by(id=12).one()

car12.car_item_pic = "static/uploads/nissan_juke_blue.jpg"

session.add(car12)
session.commit()

car13 = session.query(Car_Item).filter_by(id=13).one()

car13.car_item_pic = "static/uploads/buick_cascada_grey.jpg"

session.add(car13)
session.commit()

car14 = session.query(Car_Item).filter_by(id=14).one()

car14.car_item_pic = "static/uploads/mini_convertible_brown.jpg"

session.add(car14)
session.commit()

car15 = session.query(Car_Item).filter_by(id=15).one()

car15.car_item_pic = "static/uploads/lambo_aventador_red.jpg"

session.add(car15)
session.commit()

car16 = session.query(Car_Item).filter_by(id=16).one()

car16.car_item_pic = "static/uploads/maserati_granturismo_grey.jpg"

session.add(car16)
session.commit()

car17 = session.query(Car_Item).filter_by(id=17).one()

car17.car_item_pic = "static/uploads/alfaromeo_4c_green.jpg"

session.add(car17)
session.commit()

car18 = session.query(Car_Item).filter_by(id=18).one()

car18.car_item_pic = "static/uploads/astonmartin_vanquish_green.jpg"

session.add(car18)
session.commit()

car19 = session.query(Car_Item).filter_by(id=19).one()

car19.car_item_pic = "static/uploads/chevy_colorado_black.jpg"

session.add(car19)
session.commit()

car20 = session.query(Car_Item).filter_by(id=20).one()

car20.car_item_pic = "static/uploads/ford_f150_white.jpg"

session.add(car20)
session.commit()

car21 = session.query(Car_Item).filter_by(id=21).one()

car21.car_item_pic = "static/uploads/chrysler_pacifica_red.jpeg"

session.add(car21)
session.commit()

car22 = session.query(Car_Item).filter_by(id=22).one()

car22.car_item_pic = "static/uploads/dodge_grandcaravan_silver2.jpg"

session.add(car22)
session.commit()


car23 = session.query(Car_Item).filter_by(id=23).one()

car23.car_item_pic = "static/uploads/toyota_highlander_red.jpg"

session.add(car23)
session.commit()

car24 = session.query(Car_Item).filter_by(id=24).one()

car24.car_item_pic = "static/uploads/mazda_cx5_orange.jpg"

session.add(car24)
session.commit()

car25 = session.query(Car_Item).filter_by(id=25).one()

car25.car_item_pic = "static/uploads/landrover_green.jpg"

session.add(car25)
session.commit()

car26 = session.query(Car_Item).filter_by(id=26).one()

car26.car_item_pic = "static/uploads/mitsubishi_outlander_white.jpg"

session.add(car26)
session.commit()

print "all pics added!"
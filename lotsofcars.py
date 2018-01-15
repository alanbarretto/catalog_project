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

# Create dummy user
User1 = User(name="Robo Alan", email="tinnyTim@udacity.com")
session.add(User1)
session.commit()

User2 = User(name="Robo Sylvia", email="tinnySylvia@udacity.com")

session.add(User2)
session.commit()

category1 = Category(category="Sedans")

session.add(category1)
session.commit()

category2 = Category(category="Coupes")

session.add(category2)
session.commit()

category3 = Category(category="SUVs")

session.add(category3)
session.commit()

category4 = Category(category="Crossovers")

session.add(category4)
session.commit()

category5 = Category(category="Wagons/Hatchbacks")

session.add(category5)
session.commit()

category6 = Category(category="GreenCars/Hybrids")

session.add(category6)
session.commit()

category7 = Category(category="Convertibles")

session.add(category7)
session.commit()

category8 = Category(category="Luxury Cars")

session.add(category8)
session.commit()

category9 = Category(category="Sports Cars")

session.add(category9)
session.commit()

category10 = Category(category="Pickup Trucks")

session.add(category10)
session.commit()

category11 = Category(category="Vans/Minivans")

session.add(category11)
session.commit()


car1 = Car_Item(user_id=1, make="Toyota", model="Prius", color="blue", year="2017", price="24,500", description="This is good for long drives", milage="235", category_id=6, garage_id=1)

session.add(car1)
session.commit()

car2 = Car_Item(user_id=1, make="Toyota", model="Prius", color="orange", year="2015", price="21,045", description="Great milage.  Lots of fun on the road!", milage="12,543", category_id=6)

session.add(car2)
session.commit()

car3 = Car_Item(user_id=1, make="Acura", model="TLX", color="red", year="2018", price="33,000", description="Real luxury is fun to drive", milage="4365", category_id=1)

session.add(car3)
session.commit()

car4 = Car_Item(user_id=1, make="Audi", model="A3", color="yellow", year="2018", price="43,650", description="This is the best car I've ever driven", milage="2431", category_id=1, garage_id=1)

session.add(car4)
session.commit()


car5 = Car_Item(user_id=1, make="Ford", model="Fusion", color="black", year="2017", price="22,610", description="Sleek and stylish", milage="4621", category_id=2)

session.add(car5)
session.commit()

car6 = Car_Item(user_id=1, make="BMW", model="M2", color="Teal", year="2018", price="67,700", description="This is the ultimate driving machine! ", milage="143", category_id=2, garage_id=1)

session.add(car6)
session.commit()

car7 = Car_Item(user_id=1, make="Jeep", model="Compass", color="white", year="2017", price="32,000", description="Great for offroad trips, which is never!", milage="42", category_id=3)

session.add(car7)
session.commit()

car8 = Car_Item(user_id=2, make="Ford", model="Explorer", color="red", year="2017", price="43,600", description="When you want to look rich but can't afford an Escalade", milage="342", category_id=3, garage_id=2)

session.add(car8)
session.commit()

car9 = Car_Item(user_id=1, make="Nissan", model="Pathfinder", color="green", year="2018", price="43,530", description="Yes, they still make these things", milage="321", category_id=4)

session.add(car9)
session.commit()

car10 = Car_Item(user_id=1, make="Chevrolet", model="Traverse", color="orange", year="2016", price="35,250", description="Most awarded in its class!", milage="4323", category_id=4)

session.add(car10)
session.commit()

car11 = Car_Item(user_id=1, make="Kia", model="Niro", color="red", year="2015", price="22,543", description="When you don't care what others think", milage="6759", category_id=5, garage_id=1)

session.add(car11)
session.commit()

car12 = Car_Item(user_id=1, make="Nissan", model="Juke", color="blue", year="2017", price="18,453", description="It's a Juke!  It's not a Joke!", milage="3412", category_id=5)

session.add(car12)
session.commit()

car13 = Car_Item(user_id=1, make="Buick", model="Cascada", color="grey", year="2017", price="32,231", description="There's a car for everyone!", milage="1243", category_id=7)

session.add(car13)
session.commit()

car14 = Car_Item(user_id=1, make="Mini", model="Convertible", color="brown", year="2017", price="13,253", description="I'm a BMW too!", milage="1563", category_id=7, garage_id=1)

session.add(car14)
session.commit()

car15 = Car_Item(user_id=1, make="Lamborghini", model="Aventador", color="red", year="2016", price="76,453", description="If you can't pronounce it, you probably can't afford it", milage="7648", category_id=8)

session.add(car15)
session.commit()

car16 = Car_Item(user_id=1, make="Maserati", model="GranTurismo", color="grey", year="2018", price="94,584", description="When you want to look cool.", milage="6584", category_id=8)

session.add(car16)
session.commit()

car17 = Car_Item(user_id=1, make="Alpha Romeo", model="4C", color="green", year="2018", price="75,394", description="This is the stuff dreams are made of.", milage="6497", category_id=9)

session.add(car17)
session.commit()

car18 = Car_Item(user_id=1, make="Aston Martin", model="Vanquish", color="green", year="2015", price="243,843", description="You too can be Bond, James Bond", milage="12,342", category_id=9)

session.add(car18)
session.commit()

car19 = Car_Item(user_id=1, make="Chevy", model="Colorado", color="black", year="2018", price="25,435", description="Yeah, Baby! You're driving now!", milage="7349", category_id=10)

session.add(car19)
session.commit()

car20 = Car_Item(user_id=1, make="Ford", model="F-150", color="white", year="2017", price="27,380", description="The most durable truck in its class", milage="7342", category_id=10)

session.add(car20)
session.commit()

car21 = Car_Item(user_id=1, make="Chrysler", model="Pacifica", color="red", year="2014", price="18,435", description="The best plug in mini van!", milage="5743", category_id=11)

session.add(car21)
session.commit()

car22 = Car_Item(user_id=1, make="Dodge", model="Grand Caravan", color="silver", year="2019", price="32,934", description="Join the caravan of love!", milage="3424", category_id=11)

session.add(car22)
session.commit()


car23 = Car_Item(user_id=2, make="Toyota", model="Highlander", color="red", year="2015", price="32,934", description="Rugged yet stylish. Great for any occasion", milage="3724", category_id=3, garage_id=2)

session.add(car23)
session.commit()

car24 = Car_Item(user_id=2, make="Mazda", model="CX-5", color="orange", year="2017", price="32,984", description="Zoom zoom!  This thing gets you going!", milage="3494", category_id=3, garage_id=2)

session.add(car24)
session.commit()

car25 = Car_Item(user_id=2, make="Range Rover", model="Land Rover", color="green", year="2016", price="42,934", description="This machine is tough as nails!", milage="3424", category_id=3, garage_id=2)

session.add(car25)
session.commit()

car26 = Car_Item(user_id=2, make="Mitsubishi", model="Outlander", color="white", year="2014", price="22,934", description="Even Ninja's like driving this.", milage="14424", category_id=3, garage_id=2)

session.add(car26)
session.commit()

garage1 = Garage(name="Blue Chip Garage", user_id=1, garage_description="Great Cars, great prices! Check them out!!!")

session.add(garage1)
session.commit()

garage2 = Garage(name="Slyvia's SUV Heaven", user_id=2, garage_description="If you are looking for SUVs, you've come to the right place!")

session.add(garage2)
session.commit()


print "added all cars!"













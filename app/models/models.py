from sqlalchemy import create_engine, Column,String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

# Creating connection with Data Base
db = create_engine("sqlite:///banco.db")

#creating the Base of the Data Base
Base = declarative_base()

# Creating the Classes/Tables of Data Base

#Class of Users
class User(Base):
    """
    Creates the tables for users in DataBase
    The variable id is automatically created based on the identification of the DataBase table
    """
    __tablename__ = "users"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    name = Column("name", String)
    email = Column("email", String, nullable=False)
    password = Column("password", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)

    def __init__(self, name, email, password, active=True, admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.active = active
        self.admin = admin


#Class of Orders
class  Order(Base):
    """
    Creates the table for orders in DataBase
    Variable Status has specified values (PENDENT,CANCELED AND FINISHED), the DataBase will accept only this 3 String Values.
    Variable ID automatically created Based on the identification of the DataBase table
    """
    __tablename__ = "orders"


    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #Pendent, Canceled, Finished
    user =  Column("user", ForeignKey("users.id"))
    price = Column("price", Float)
    items = relationship("ItemOrdered", cascade="all, delete")
    #items =
    def __init__(self, user, status="PENDENT", price=0):
        self.user = user
        self.status = status
        self.price = price

    def calculate_price(self):
        order_price = 0
        for item in self.items:
            item_price = item.unit_price * item.amount
            order_price += item_price
        self.price = order_price


#Items Ordered
class ItemOrdered(Base):
    """
    Creates the table for Items Ordered in DataBase
    Variable ID automatically created Based on the identification of the DataBase table
    """

    __tablename__ = "items_ordered"

    id = Column("id", Integer, primary_key=True, autoincrement=True)
    amount = Column("amount", Integer)
    flavor = Column("flavor", String)
    size = Column("size", String)
    unit_price = Column("unit_price", Float)
    order = Column("order", ForeignKey("orders.id"))

    def __init__(self, amount, flavor, size, unit_price, order):
        self.amount = amount
        self.flavor = flavor
        self.size = size
        self.unit_price = unit_price
        self.order = order
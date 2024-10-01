from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import Depends
from main import Base
from models.item import Item
from database import get_db

# Add items to database
def populate_data():
    db = next(get_db())
    items = [
        Item(name="Book", price=100, stock=500),
        Item(name="Apple", price=5, stock=500),
        Item(name="Car", price=10000, stock=50),
        Item(name="Bike", price=2000, stock=150),
    ]
    db.add_all(items)
    db.commit()
    db.close()


populate_data()

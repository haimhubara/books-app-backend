import json
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Products  
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL =  os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)


with open("data/db.json", "r", encoding="utf-8") as f:
    data = json.load(f)

products_list = data["products"]  

for p in products_list:
    product = Products(
        id=p["id"],
        name=p["name"],
        overview=p.get("overview"),
        long_description=p.get("long_description"),
        price=p["price"],
        poster=p.get("poster"),
        image_local=p.get("image_local"),
        rating=p.get("rating"),
        in_stock=p.get("in_stock", True),
        size=p.get("size"),
        best_seller=p.get("best_seller", False)
    )
    session.add(product)

session.commit()
print("All products added successfully!")
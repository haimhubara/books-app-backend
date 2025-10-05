from src.models import Base, Users
from src.database import  engine
from passlib.context import CryptContext
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL =  os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

Base.metadata.create_all(engine)

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


guest_email = "guest@gmail.com"
guest_name = "Guest User"
guest_password = "12345678"

user = session.query(Users).filter(Users.email == guest_email).first()
if not user:
    new_user = Users(
        email=guest_email,
        name=guest_name,
        hashed_password=bcrypt_context.hash(guest_password)
    )
    session.add(new_user)
    session.commit()
    print("Guest user created successfully!")
else:
    print("Guest user already exists.")

session.close()

from fastapi import FastAPI
from src.routers import  data, auth, products
from fastapi.middleware.cors import CORSMiddleware
from src.database import Base,engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000", 
    "https://haimhubara-books-web.netlify.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       
    allow_credentials=True,
    allow_methods=["GET", "POST"] ,        
    allow_headers=["Authorization", "Content-Type"]   
)


app.include_router(data.router)
app.include_router(auth.router)
app.include_router(products.router)



from datetime import datetime
from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status,Path
from sqlalchemy.orm import Session, joinedload
from pydantic import BaseModel
from routers.auth import get_current_user

from database import SessionLocal
from models import Users, Orders, OrderItems, Products

router = APIRouter(tags=["Orders"])

# ------------------ Database Dependency ------------------
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]

# ------------------ Schemas ------------------
class UserOut(BaseModel):
    id: int
    email: str
    name:str
    
    class Config:
        from_attributes = True

class OrderItemCreate(BaseModel):
    product_id: int
    quantity: int = 1
    price: float

class OrderCreate(BaseModel):
    amount_paid: float
    items: List[OrderItemCreate]


class ProductInOrderOut(BaseModel):
    id: int
    name: str
    overview: str
    long_description: str
    price: float
    poster: str
    image_local: str
    rating: int
    in_stock: bool
    size: int
    best_seller: bool

    class Config:
        from_attributes = True

class OrderSimpleOut(BaseModel):
    id: int
    cartList: List[ProductInOrderOut]
    amount_paid: float
    user:UserOut
    quantity: int

class OrderSimpleOutV2(BaseModel):
    id: int
    cartList: List[ProductInOrderOut]
    amount_paid: float
    quantity: int


    class Config:
        from_attributes = True

# ------------------ Routes ------------------
@router.get("/660/orders", response_model=List[OrderSimpleOutV2], status_code=status.HTTP_200_OK)
def get_user_orders(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail="Authenticate Fail.")

    orders = db.query(Orders).options(joinedload(Orders.items).joinedload(OrderItems.product))\
               .filter(Orders.user_id == user["id"]).all()

    result = []
    for order in orders:
        cart_list = [item.product for item in order.items] 
        result.append(OrderSimpleOutV2(
            id=order.id,
            cartList=cart_list,
            amount_paid=order.amount_paid,
            quantity=len(cart_list),
        ))
    return result

@router.post("/660/orders", response_model=OrderSimpleOut, status_code=status.HTTP_201_CREATED)
def create_order(order: OrderCreate, db: db_dependency, current_user:user_dependency):
    if current_user is None:
        raise HTTPException(status_code=401, detail="Authenticate Fail.")
    
    new_order = Orders(
        user_id=current_user["id"],
        amount_paid=order.amount_paid,
        quantity=len(order.items)
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    cart_list = []
    for item in order.items:
        db_item = OrderItems(
            order_id=new_order.id,
            product_id=item.product_id,
            quantity=item.quantity,
            price=item.price
        )
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        product = db.query(Products).filter(Products.id == item.product_id).first()
        cart_list.append(ProductInOrderOut.from_orm(product))

    user = db.query(Users).filter(Users.id == new_order.user_id).first()

    return OrderSimpleOut(
        id=new_order.id,
        cartList=cart_list,
        amount_paid=new_order.amount_paid,
        quantity=new_order.quantity,
        user=UserOut.from_orm(user)
    )

@router.get("/600/users/{uid}", response_model=UserOut, status_code=status.HTTP_200_OK)
async def get_user(
    uid: int = Path(..., description="The ID of the user to retrieve"),
    current_user: dict = Depends(get_current_user),
    db: db_dependency = db_dependency
):
    if current_user["id"] != uid:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")

    user = db.query(Users).filter(Users.id == uid).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return UserOut.from_orm(user)  
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import create_session
from schemas import OrderSchema
from models import Order
order_router = APIRouter(prefix="/orders", tags=["orders"]) #Create a route for ordering

@order_router.get("/")
async def orders():
    """
    This is the Standart route of Order. Every orders routes needs authenticated users.
    :return:
    """
    return {"mensage": "You accesed the standart order route"}

@order_router.post("/order")
async def create_order(order_schema: OrderSchema, session = Depends(create_session)):
    """
    :return:
    """
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {"mensage": f"Order created successfully. Order ID: {new_order.id}"}
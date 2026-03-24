from fastapi import APIRouter

order_router = APIRouter(prefix="/orders", tags=["orders"]) #Create a route for ordering

@order_router.get("/")
async def orders():
    """
    This is the Standart route of Order. Every orders routes needs authenticated users.
    :return:
    """
    return {"mensage": "You accesed the standart order route"}
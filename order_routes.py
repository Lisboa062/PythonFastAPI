
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import create_session, verify_token
from schemas import OrderSchema, ItemOrderSchema, ResponseOrderSchema
from models import Order, User, ItemOrdered


order_router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)]) #Create a route for ordering


@order_router.post("/")
async def create_order(order_schema: OrderSchema, session: Session = Depends(create_session)):
    """
    A Standart route to first of all create an order in the DataBase, only authenticated users can do this.
    :return:Mensage with the Order ID
    """
    new_order = Order(user=order_schema.user)
    session.add(new_order)
    session.commit()
    return {"mensage": f"Order created successfully. Order ID: {new_order.id}"}


@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to cancel an order. Only the user owner of the order or the admin can do this.
    :param id_order: Identification of order
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the order id that was canceled successfully.
    """
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You are not authorized to do this modification.")
    order.status = "CANCELED"
    session.commit()
    return {"mensage": f"Order number {order.id} canceled successfully.",
            "order": order
            }


@order_router.get("/list")
async def list_orders(session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route just to list every Order listed in DataBase, Only Users Admins can do it.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Orders
    """
    if not user.admin:
        raise HTTPException(status_code=401, detail="You are not allowed to do this.")
    else:
        orders = session.query(Order).all()
        return {
            "orders": orders}


@order_router.post("/order/add-item/{order_id}")
async def add_item_order(order_id: int, item_order_schema: ItemOrderSchema, session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to Add Items to the order. Only the User Owner of the Order and Users Admin can do it.
    :param order_id: Receive the Order to add the item.
    :param item_order_schema: Standard package of information about the item.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the item id and the price of the order
    """
    order = session.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You are not allowed to do this.")
    item_ordered = ItemOrdered(item_order_schema.amount, item_order_schema.flavor, item_order_schema.size, item_order_schema.unit_price,order_id)
    session.add(item_ordered)
    order.calculate_price()
    session.commit()
    return {
        "mensage": "Item created successfully",
        "item_id": item_ordered.id,
        "price_ordered": order.price
    }


@order_router.post("/order/remove-item/{item_order_id}")
async def remove_item_order(item_order_id: int, session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to remove an Item of the Order.
    :param item_order_id: Receive the item id that user wish to remove
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the Items that keep in the order and the order complete.
    """
    item_ordered = session.query(ItemOrdered).filter(ItemOrdered.id == item_order_id).first()
    order = session.query(Order).filter(Order.id==item_ordered.order).first()
    if not item_ordered:
        raise HTTPException(status_code=400, detail="Item in Order Not Found.")
    if not user.admin and user.id != item_ordered.order.user:
        raise HTTPException(status_code=401, detail="You are not allowed to do this.")
    session.delete(item_ordered)
    order.calculate_price()
    session.commit()
    return {
        "mensage": "Item removed successfully",
        "items_order": order.items,
        "Order": order
    }


@order_router.post("/order/finish/{id_order}")
async def finish_order(id_order: int, session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to finish the order. Only user owner of the order os Admin can do this.
    :param id_order: order id to finish.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the order id that was finished and the order itself.
    """
    order = session.query(Order).filter(Order.id==id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You are not authorized to do this modification.")
    order.status = "FINISHED"
    session.commit()
    return{
        "mensage": f"Order number {order.id} finished successfuly.",
        "order": order
    }

@order_router.get("/order/{id_order}")
async def inspect_order(id_order: int, session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to inspect a determinate order.
    :param id_order: order id to inspect.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Just the amount of items ordered and the order itself.
    """
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")
    if not user.admin and user.id != order.user:
        raise HTTPException(status_code=401, detail="You are not authorized to do this modification.")
    return{
        "Amount of items ordered": len(order.items),
        "order": order
    }


@order_router.get("/list-user", response_model=ResponseOrderSchema)
async def list_orders(session: Session = Depends(create_session), user: User = Depends(verify_token)):
    """
    Route to list all Orders of the user authenticated.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: All Orders
    """
    orders = session.query(Order).filter(Order.user == user.id).all()
    return orders
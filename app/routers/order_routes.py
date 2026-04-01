from fastapi import APIRouter, Depends, HTTPException

from app.core.exceptions import (OrderNotFoundException, 
                                 NotAuthorizedException,
                                 ItemNotFoundException)

from sqlalchemy.orm import Session

from app.dependencies import (create_session,
                              get_current_user)

from app.schemas.schemas import (OrderCreate, 
                                 ItemOrderSchema, 
                                 ResponseOrderSchema)

from app.models.models import (Order, 
                               User, 
                               ItemOrdered)

from app.services.order_service import (create_order_service, 
                                        cancel_order_service,
                                        finish_order_service,
                                        inspect_order_service,
                                        list_orders_admin_service,
                                        list_orders_service,
                                        add_item_service,
                                        remove_item_order_service)

from app.repositories.order_repository import (get_orders_by_user_id,)




order_router = APIRouter(prefix="/orders",
                          tags=["orders"], 
                          dependencies=[Depends(get_current_user)]) #Create a route for ordering


@order_router.post("/")
async def create_order(order: OrderCreate, 
                       session: Session = Depends(create_session), 
                       current_user = Depends(get_current_user)):
    """
    A Standart route to first of all create an order in the DataBase, only authenticated users can do this.
    :param current_user: Use the current user to create the order or if is admin choose one user.
    :return:Message with the Order ID
    """
    
    try:
        new_order = create_order_service(session = session, 
                                        current_user = current_user, 
                                        order_data = order)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not authorized to do this.")
    
    return {"message": f"Order created successfully. Order ID: {new_order.id}"}


@order_router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, 
                       session: Session = Depends(create_session), 
                       user: User = Depends(get_current_user), ):
    """
    Route to cancel an order. Only the user owner of the order or the admin can do this.
    :param id_order: Identification of order
    :param session: Open a connection with DataBase
    :param user_id: Check if the user is authenticated.
    :return: Message with the order id that was canceled successfully.
    """
    try:
        order = cancel_order_service(session=session, 
                                    current_user=user, 
                                    order_id=id_order)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not authorized to do this.")

    return {"mensage": f"Order number {order.id} canceled successfully.",
            "order": order
            }


@order_router.get("/list")
async def list_orders(session: Session = Depends(create_session), 
                      user: User = Depends(get_current_user)):
    """
    Route just to list every Order listed in DataBase, Only Users Admins can do it.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Orders
    """
    try:
        orders = list_orders_admin_service(session=session, current_user=user)
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not Authorized to do this.")
    
    return {"orders": orders}


@order_router.post("/order/add-item/{order_id}")
async def add_item_order(order_id: int, 
                         item_order_schema: ItemOrderSchema, 
                         session: Session = Depends(create_session), 
                         user: User = Depends(get_current_user)):
    """
    Route to Add Items to the order. Only the User Owner of the Order and Users Admin can do it.
    :param order_id: Receive the Order to add the item.
    :param item_order_schema: Standard package of information about the item.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the item id and the price of the order
    """
    try:
        item_ordered, order = add_item_service(session=session,
                                            current_user=user,
                                            order_id=order_id,
                                            item_data=item_order_schema)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not Authorized to do this.")

    return {
        "mensage": "Item created successfully",
        "item_id": item_ordered.id,
        "price_ordered": order.price
    }


@order_router.post("/order/remove-item/{item_order_id}")
async def remove_item_order(item_order_id: int, 
                            session: Session = Depends(create_session), 
                            user: User = Depends(get_current_user)):
    """
    Route to remove an Item of the Order.
    :param item_order_id: Receive the item id that user wish to remove
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the Items that keep in the order and the order complete.
    """
    try:
        order = remove_item_order_service(session=session, current_user=user, item_order_id=item_order_id)
    except ItemNotFoundException:
        raise HTTPException(status_code=400, detail="Item Not Found.")
    
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not authorized to do this.")

    return {
        "mensage": "Item removed successfully",
        "items_order": order.items,
        "Order": order
    }


@order_router.post("/order/finish/{id_order}")
async def finish_order(id_order: int, 
                       session: Session = Depends(create_session), 
                       user: User = Depends(get_current_user)):
    """
    Route to finish the order. Only user owner of the order os Admin can do this.
    :param id_order: order id to finish.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Message with the order id that was finished and the order itself.
    """
    try:
        order = finish_order_service(session=session, 
                                    current_user=user, 
                                    order_id=id_order)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not Authorized to do this.")

    return{
        "mensage": f"Order number {order.id} finished successfuly.",
        "order": order
    }

@order_router.get("/order/{id_order}")
async def inspect_order(id_order: int, 
                        session: Session = Depends(create_session), 
                        user: User = Depends(get_current_user)):
    """
    Route to inspect a determinate order.
    :param id_order: order id to inspect.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: Just the amount of items ordered and the order itself.
    """
    try:
        order = inspect_order_service(session=session, 
                                    order_id=id_order, 
                                    current_user=user)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")
    
    except NotAuthorizedException:
        raise HTTPException(status_code=401, detail="You are not Authorized to do this.")

    return{
        "Amount of items ordered": len(order.items),
        "order": order
    }


@order_router.get("/list-user", response_model=list[ResponseOrderSchema])
async def list_orders(session: Session = Depends(create_session), 
                      user: User = Depends(get_current_user)):
    """
    Route to list all Orders of the user authenticated.
    :param session: Open a connection with DataBase
    :param user: Check if the user is authenticated
    :return: All Orders
    """
    try:
        orders = list_orders_service(session=session,
                                    current_user=user)
    except OrderNotFoundException:
        raise HTTPException(status_code=400, detail="Order Not Found.")

    return orders
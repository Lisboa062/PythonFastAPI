from app.repositories.order_repository import (create_order, 
                                               get_order_by_id)

from fastapi import HTTPException


def validate_order_permission(current_user, order):
    if not current_user.admin and current_user.id != order.user_id:
        raise HTTPException(status_code=401, 
                            detail="You are not authorized to do this modification.")


def create_order_service(session, 
                         current_user, 
                         order_data):
    
    if current_user.admin and order_data.user_id:
        user_id = order_data.user_id
    else:
        user_id = current_user.id
    
    return create_order(session, user_id)


def cancel_order_service(session, 
                         current_user, 
                         order_id):

    order = get_order_by_id(session=session, order_id=order_id)

    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")
    
    validate_order_permission(current_user=current_user, order=order)
    
    order.status = "CANCELED"
    session.commit()
    session.refresh(order)
    return order


def finish_order_service(session, 
                         order_id, 
                         current_user):
    
    order = get_order_by_id(session=session, order_id=order_id)

    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")

    validate_order_permission(current_user=current_user, order=order)

    order.status = "FINISHED"
    session.commit()
    session.refresh(order)
    return order


def inspect_order_service(session, 
                          order_id, 
                          current_user):
    
    order = get_order_by_id(session=session, order_id=order_id)

    if not order:
        raise HTTPException(status_code=400, detail="Order not Found.")
    
    validate_order_permission(current_user=current_user, order=order)
    
    return order
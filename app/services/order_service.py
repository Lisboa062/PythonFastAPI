from app.repositories.order_repository import (create_order, 
                                               get_order_by_id,
                                               get_all_orders,)

from app.core.exceptions import (OrderNotFoundException, 
                                 NotAuthorizedException,)

from fastapi import HTTPException


def validate_admin(current_user):
    if not current_user.admin:
        raise NotAuthorizedException()
    return True


def validate_order_permission(current_user, order):
    if not current_user.admin and current_user.id != order.user_id:
        raise NotAuthorizedException()


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
        raise OrderNotFoundException()
    
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
        raise OrderNotFoundException()

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
        raise OrderNotFoundException()
    
    validate_order_permission(current_user=current_user, order=order)
    
    return order


def list_orders(session,
                current_user):
    
    orders = get_all_orders(session=session)
    if validate_admin(current_user=current_user):
        return orders

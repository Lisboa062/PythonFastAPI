from app.repositories.order_repository import (create_order, 
                                               get_order_by_id,
                                               get_all_orders,
                                               get_orders_by_user_id)

from app.repositories.item_repository import (create_item_ordered, 
                                              get_item_by_id,
                                              delete_item_ordered,)

from app.core.exceptions import (OrderNotFoundException, 
                                 NotAuthorizedException,
                                 ItemNotFoundException,)


def validate_admin(current_user):
    if not current_user.admin:
        raise NotAuthorizedException()


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


def list_orders_admin_service(session,
                current_user):
    
    orders = get_all_orders(session=session)
    validate_admin(current_user=current_user)
    return orders


def list_orders_service(session, current_user):
    orders = get_orders_by_user_id(session=session, user_id=current_user.id)

    if not orders:
        raise OrderNotFoundException()
    

    return orders
    


def add_item_service(session, current_user, order_id, item_data):

    order = get_order_by_id(session=session, order_id=order_id)

    if not order:
        raise OrderNotFoundException()
    
    validate_order_permission(current_user=current_user, order=order)
    
    item_ordered = create_item_ordered(session=session, 
                                       item_data=item_data, 
                                       order_id=order_id)

    order.calculate_price()
    session.commit()
    session.refresh(item_ordered)
    session.refresh(order)

    return item_ordered, order


def remove_item_order_service(session, current_user, item_order_id):
    item_ordered = get_item_by_id(session=session, item_order_id=item_order_id)

    if not item_ordered:
        raise ItemNotFoundException()
    
    order = get_order_by_id(session=session,order_id=item_ordered.order)

    if not order:
        raise OrderNotFoundException()
    
    validate_order_permission(current_user=current_user, order=order)

    delete_item_ordered(session=session, item_ordered=item_ordered)
    order.calculate_price()
    session.commit()
    session.refresh(order)

    return order
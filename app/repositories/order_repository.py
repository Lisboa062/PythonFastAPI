from app.models.models import (Order, 
                               ItemOrdered)
                               


def create_order(session, user_id):
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order


def get_order_by_id(session, order_id):
    return session.query(Order).filter(Order.id==order_id).first()


def get_orders_by_user_id(session, user_id):
    return session.query(Order).filter(Order.user == user_id).all()


def get_all_orders(session):
    return session.query(Order).all()



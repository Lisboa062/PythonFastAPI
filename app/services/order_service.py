from app.models.models import Order

def create_order_service(session, user_id):
    order = Order(user_id=user_id)
    session.add(order)
    session.commit()
    session.refresh(order)
    return order

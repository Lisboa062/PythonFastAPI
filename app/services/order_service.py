from app.repositories.order_repository import create_order

def create_order_service(session, current_user, order_data):
    if current_user.admin and order_data.user_id:
        user_id = order_data.user_id
    else:
        user_id = current_user.id
    
    return create_order(session, user_id)

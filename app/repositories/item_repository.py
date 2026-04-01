from app.models.models import ItemOrdered


def get_item_by_id(session, item_order_id):
    return session.query(ItemOrdered).filter(ItemOrdered.id == item_order_id).first()
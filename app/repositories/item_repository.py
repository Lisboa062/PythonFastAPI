from app.models.models import ItemOrdered


def get_item_by_id(session, item_order_id):
    return session.query(ItemOrdered).filter(ItemOrdered.id == item_order_id).first()


def delete_item_ordered(session, item_ordered):
    session.delete(item_ordered)


def create_item_ordered(session, item_data, order_id):
    
    item_ordered = ItemOrdered(
        item_data.amount,
        item_data.flavor,
        item_data.size,
        item_data.unit_price,
        order_id
    )
    session.add(item_ordered)
    session.flush()
    return item_ordered

from app.models.models import User


def get_user_by_email(user_schema, session):
    return session.query(User).filter(User.email == user_schema.email).first()
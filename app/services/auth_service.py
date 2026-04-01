from app.models.models import User
from app.schemas.schemas import UserSchema
from sqlalchemy.orm import Session
from app.core.security import bcrypt_context
from app.core.exceptions import EmailUsedException
from app.repositories.auth_repository import get_user_by_email


def authenticator_user(email, password, session):
    """
    Functin that verify if the email and password sent by the user exist in DataBase or if is correspondent to the email and cryptography password.
    :param email: email to check
    :param password: password to check
    :param session: Open a connection with DataBase
    :return: The user to log in.
    """
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return None
    elif not bcrypt_context.verify(password, user.password):
        return None
    else:
        return user
    

def create_account_service(user_schema: UserSchema, session: Session) -> User:

    existing_user = get_user_by_email(user_schema=user_schema, session=session)

    if existing_user:
        raise EmailUsedException()
    
    crypt_password = bcrypt_context.hash(user_schema.password)
    new_user = User(
        user_schema.name,
        user_schema.email,
        crypt_password,
        user_schema.active,
        user_schema.admin,
    )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user
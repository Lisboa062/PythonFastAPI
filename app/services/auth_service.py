from app.models.models import User
from app.schemas.schemas import UserSchema
from sqlalchemy.orm import Session
from app.core.security import bcrypt_context
from app.core.exceptions import EmailUsedException, InvalidCredentialsException
from app.repositories.auth_repository import (get_user_by_email, 
                                              create_user)
from app.core.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from datetime import datetime, timedelta, timezone
from jose import jwt


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
        raise InvalidCredentialsException()
    elif not bcrypt_context.verify(password, user.password):
        raise InvalidCredentialsException()
    else:
        return user
    

def create_account_service(user_schema: UserSchema, session: Session) -> User:

    existing_user = get_user_by_email(email=user_schema.email, session=session)

    if existing_user:
        raise EmailUsedException()
    
    crypt_password = bcrypt_context.hash(user_schema.password)

    return create_user(session=session, user_schema=user_schema, crypt_password=crypt_password)


def create_access_token(user_id) -> str:
    """
    Function to create encoded tokens based on the user id and time of expiration. Token standard JWT.
    :param user_id: user owner of token
    :param token_time: time of expiration of token.
    :return: encode token
    """
    expiration_date = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    dic_info = {"sub": str(user_id), 
                "type": "access",
                "exp": expiration_date}
    
    return jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)


def create_refresh_token(user_id) -> str:
        """
        Function to create encoded tokens based on the user id and time of expiration. Token standard JWT.
        :param user_id: user owner of token
        :param token_time: time of expiration of token.
        :return: encode token
        """
        expiration_date = datetime.now(timezone.utc) + timedelta(days=7)

        dic_info = {"sub": str(user_id), 
                    "type": "refresh",
                    "exp": expiration_date}
        
        return jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)

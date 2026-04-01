from sqlalchemy.orm import sessionmaker, Session
from app.core.config import ALGORITHM, SECRET_KEY
from app.core.security import oauth2_schema
from app.models.models import db, User
from fastapi import Depends, HTTPException
from jose import jwt, JWTError


def create_session():
    """
    Function used to Open and Close a connection with DataBase.
    :return: session of connection.
    """
    try:
        sessions = sessionmaker(bind=db)  # Create a connection beetwen DataBase and the Router
        session = sessions()  # open 1 instance of this connection
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(oauth2_schema), session: Session = Depends(create_session)):
    """
    Check the id of the current user authenticated.
    """

    dic_info = get_token_dic(token=token)

    user_id = dic_info.get("sub")
    token_type = dic_info.get("type")


    if user_id is None or token_type != "access":
        raise HTTPException(status_code=401, details="Invalid Access Token.")
    
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, details="User Not Found.")
    
    return user


def get_current_refresh_user(token: str = Depends(oauth2_schema), session: Session = Depends(create_session)):
    """
    Check the id of the current user authenticated.
    """

    dic_info = get_token_dic(token=token)

    user_id = dic_info.get("sub")
    token_type = dic_info.get("type")


    if user_id is None or token_type != "refresh":
        raise HTTPException(status_code=401, details="Invalid Refresh Token.")
    
    user = session.query(User).filter(User.id == user_id).first()

    if not user:
        raise HTTPException(status_code=401, details="User Not Found.")
    
    return user


def get_token_dic(token:str):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        return dic_info
    except JWTError:
        raise HTTPException(status_code=401, details="Invalid Authentication.")
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

    try:
        dic_info = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        user_id = dic_info.get("sub")

        if user_id is None:
            raise HTTPException(status_code=401, details="Invalid Authentication.")
        
    except JWTError:
        raise HTTPException(status_code=401, details="Invalid Authentication.")
    
    user = session.query(User).filter(User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=401, details="User Not Found.")
    
    return user
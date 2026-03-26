from sqlalchemy.orm import sessionmaker, Session

from app.main import ALGORITHM, SECRET_KEY, oauth2_schema
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


def verify_token(token: str = Depends(oauth2_schema), session: Session = Depends(create_session)):
    """
    Function to verify if the token sent is valid.
    :param token: token sent to verify
    :param session: Open a connection with DataBase
    :return: The user that had de token verified.
    """
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Access denied.")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid access.")
    return user
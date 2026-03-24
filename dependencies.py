from sqlalchemy.orm import sessionmaker
from models import db


def create_session():
    try:
        sessions = sessionmaker(bind=db)  # Create a connection beetwen DataBase and the Router
        session = sessions()  # open 1 instance of this connection
        yield session
    finally:
        session.close()
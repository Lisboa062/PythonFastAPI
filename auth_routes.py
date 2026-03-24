from fastapi import APIRouter, Depends, HTTPException

from main import bcrypt_context
from models import  User
from dependencies import create_session
from schemas import UserSchema, LoginSchema
auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Create a route for authentication

def create_token(user_id):
    token = f"fgwrevijwreiv{user_id}"
    return token

@auth_router.get("/")
async def home():
    """
    This is the standart authenticator route.
    :return:
    """
    return {"mensage": "You accesed the standart route of authenticator", "authenticator": False}

@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session = Depends(create_session)):
    user = session.query(User).filter(User.email == user_schema.email).first()
    if user:#Check if already exist a user with the same email
        raise HTTPException(status_code=400, detail="E-mail already used.")
    else:
        crypt_password = bcrypt_context.hash(user_schema.password)
        new_user = User(UserSchema.name, user_schema.email, crypt_password, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"mensage": f"user {UserSchema.email} successfully registered."}

@auth_router.post("/login")
async def login(login_schema: LoginSchema, session = Depends(create_session)):
    user = session.query(User).filter(User.email==login_schema.email).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not found.")
    else:
        access_token = create_token(user.id)
        return{"access_token": access_token,
               "token_type": "Bearer"
               }


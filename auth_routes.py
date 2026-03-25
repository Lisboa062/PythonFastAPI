from fastapi import APIRouter, Depends, HTTPException

from main import bcrypt_context, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from models import  User
from dependencies import create_session, verify_token
from schemas import UserSchema, LoginSchema
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm
auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Create a route for authentication

def create_token(user_id, token_time = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    #JWT
    expiration_date = datetime.now(timezone.utc) + token_time
    dic_info = {"sub": str(user_id), "exp":expiration_date}
    encode_jwt = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return encode_jwt


def authenticator_user(email, password, session):
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    else:
        return user


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
        new_user = User(user_schema.name, user_schema.email, crypt_password, user_schema.active, user_schema.admin)
        session.add(new_user)
        session.commit()
        return {"mensage": f"user {user_schema.email} successfully registered."}

@auth_router.post("/login-form")
async def login_form(formulary_data: OAuth2PasswordRequestForm = Depends(), session = Depends(create_session)):
    user = authenticator_user(formulary_data.username, formulary_data.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid password.")
    else:
        access_token = create_token(user.id)
        return{"access_token": access_token,
               "token_type": "Bearer"
               }


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session = Depends(create_session)):
    user = authenticator_user(login_schema.email, login_schema.password, session)
    if not user:
        raise HTTPException(status_code=400, detail="User not found or invalid password.")
    else:
        access_token = create_token(user.id)
        refresh_token = create_token(user.id, token_time=timedelta(days=7))
        return{"access_token": access_token,
               "refresh_token": refresh_token,
               "token_type": "Bearer"
               }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)
    return {"access_token": access_token,
            "token_type": "Bearer"
            }



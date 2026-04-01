from fastapi import APIRouter, Depends, HTTPException

from app.core.config import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
from app.core.security import bcrypt_context
from app.models.models import User
from app.dependencies import create_session, get_current_user
from app.schemas.schemas import UserSchema, LoginSchema
from app.services.auth_service import (authenticator_user, 
                                       create_account_service)
from jose import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordRequestForm

auth_router = APIRouter(
    prefix="/auth", tags=["auth"]
)  # Create a route for authentication


def create_token(user_id, token_time=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)):
    """
    Function to create encoded tokens based on the user id and time of expiration. Token standard JWT.
    :param user_id: user owner of token
    :param token_time: time of expiration of token.
    :return: encode token
    """
    expiration_date = datetime.now(timezone.utc) + token_time
    dic_info = {"sub": str(user_id), "exp": expiration_date}
    encode_jwt = jwt.encode(dic_info, SECRET_KEY, algorithm=ALGORITHM)
    return encode_jwt


@auth_router.post("/create_account")
async def create_account(user_schema: UserSchema, session=Depends(create_session)):
    """
    Route to create a new account in DataBase.
    :param user_schema: convertion all information to a structure and rules previously defined.
    :param session: Open a connection with DataBase
    :return: Message that the user was registered.
    """

    new_user = create_account_service(user_schema=user_schema, session=session)

    return {"message": f"user {new_user.email} successfully registered."}



@auth_router.post("/login-form")
async def login_form(
    formulary_data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(create_session),
):
    """
    Just a route to login by the form of FastAPI page.
    :param formulary_data: Information sent by the formulary of the page to login.
    :param session: Open a connection with DataBase
    :return: create and return a token for the user to be authenticated.
    """

    user = authenticator_user(email=formulary_data.username, password=formulary_data.password, session=session)

    if not user:
        raise HTTPException(
            status_code=400, detail="User not found or invalid password."
        )

    access_token = create_token(user.id)
    return {"access_token": access_token, "token_type": "Bearer"}


@auth_router.post("/login")
async def login(login_schema: LoginSchema, session=Depends(create_session)):
    """
    Route to log in and be authenticated.
    :param login_schema: structure of the information to log in.
    :param session: Open a connection with DataBase
    :return: create and return tokens for the user keep authenticated.
    """

    user = authenticator_user(email=login_schema.email, password=login_schema.password, session=session)

    if not user:
        raise HTTPException(
            status_code=400, detail="User not found or invalid password."
        )

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, token_time=timedelta(days=7))
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
    }


@auth_router.get("/refresh")
async def use_refresh_token(user: User = Depends(get_current_user)):
    """
    Route to create token.
    :param user: User to receive the token
    :return: access token
    """

    access_token = create_token(user.id)
    return {"access_token": access_token, "token_type": "Bearer"}

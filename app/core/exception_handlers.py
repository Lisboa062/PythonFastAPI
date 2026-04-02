from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import (EmailUsedException, 
                                 OrderNotFoundException, 
                                 NotAuthorizedException, 
                                 ItemNotFoundException,
                                 InvalidCredentialsException)


async def email_used_exception_handler(request: Request, exc: EmailUsedException):
    return JSONResponse(
        status_code=400,
        content={"detail": "E-mail already used."},)


async def order_not_found_handler(request: Request, exc: OrderNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail": "Order not found."},)


async def not_authorized_handler(request: Request, exc: NotAuthorizedException):
    return JSONResponse(
        status_code=403,
        content={"detail": "You are not authorized."},)


async def item_not_found_handler(request: Request, exc: ItemNotFoundException):
    return JSONResponse(
        status_code=404,
        content={"detail":"Item not found."}
    )


async def invalid_credentials_handler(request: Request, exc: InvalidCredentialsException):
    return JSONResponse(
        status_code=401,
        content={"detail":"Invalid Email or Password."}
    )
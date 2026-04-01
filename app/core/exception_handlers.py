from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.exceptions import EmailUsedException, OrderNotFoundException, NotAuthorizedException


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
        status_code=401,
        content={"detail": "Not authorized."},)
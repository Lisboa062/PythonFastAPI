from fastapi import FastAPI
from app.core.exception_handlers import (
    email_used_exception_handler,
    order_not_found_handler,
    not_authorized_handler)

from app.core.exceptions import (
    EmailUsedException,
    OrderNotFoundException,
    NotAuthorizedException)

app = FastAPI()


from app.routers.auth_routes import auth_router
from app.routers.order_routes import order_router

app.add_exception_handler(EmailUsedException, email_used_exception_handler)
app.add_exception_handler(OrderNotFoundException, order_not_found_handler)
app.add_exception_handler(NotAuthorizedException, not_authorized_handler)

app.include_router(auth_router)
app.include_router(order_router)

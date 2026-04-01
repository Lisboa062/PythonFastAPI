from fastapi import FastAPI

app = FastAPI()


from app.routers.auth_routes import auth_router
from app.routers.order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)

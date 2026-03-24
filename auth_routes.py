from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"]) #Create a route for authentication


@auth_router.get("/")
async def authenticator():
    """
    This is the standart authenticator route.
    :return:
    """
    return {"mensage": "You accesed the standart route of authenticator", "authenticator": False}

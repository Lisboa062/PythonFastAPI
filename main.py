from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from dotenv import load_dotenv
import os

from sqlalchemy.util import deprecated

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
app = FastAPI()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_schema = OAuth2PasswordBearer(tokenUrl="auth/login-form")


from auth_routes import auth_router
from order_routes import order_router

app.include_router(auth_router)
app.include_router(order_router)


# para rodar o código, executar no terminal: uvicorn main:app --reload

# endpoints: é o restante do domínio que vai responder a um determinado tipo de requisição. Ex. domínio.com/Ordens

# Rest API's = parecido com CRUD do Banco de dados/ C-Create, R-Read, U-Update, D-Delete
# Get -> leitura/pegar
# Post -> enviar/criar
# put/patch -> edição
# delete -> deletar
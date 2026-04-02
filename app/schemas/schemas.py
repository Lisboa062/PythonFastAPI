from pydantic import BaseModel, ConfigDict
from typing import Optional, List

"""
This is all objects structures used in the program.
"""

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool] = True
    admin: Optional[bool] = False

    model_config = ConfigDict(from_attributes = True)


class OrderCreate(BaseModel):
    user_id: Optional[int] = None

    model_config = ConfigDict(from_attributes = True)

class LoginSchema(BaseModel):
    email: str
    password: str

    model_config = ConfigDict(from_attributes = True)


class ItemOrderSchema(BaseModel):
    amount: int
    flavor: str
    size: str
    unit_price: float

    model_config = ConfigDict(from_attributes = True)


class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    items: List[ItemOrderSchema]
    
    model_config = ConfigDict(from_attributes = True)

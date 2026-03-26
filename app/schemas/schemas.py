from pydantic import BaseModel
from typing import Optional, List

"""
This is all objects structures used in the program.
"""

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    active: Optional[bool]
    admin: Optional[bool]

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True

class LoginSchema(BaseModel):
    email: str
    password: str

    class Config:
        from_attributes = True


class ItemOrderSchema(BaseModel):
    amount: int
    flavor: str
    size: str
    unit_price: float

    class Config:
        from_attributes = True


class ResponseOrderSchema(BaseModel):
    id: int
    status: str
    price: float
    Items: List[ItemOrderSchema]
    class Config:
        from_attributes = True

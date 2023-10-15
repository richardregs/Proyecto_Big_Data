"""
Model class User
"""
from typing import Union
from pydantic import BaseModel


class User(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    username: Union[str, None] = None
    full_name: Union[str, None] = None
    email: Union[str, None] = None
    disabled: Union[bool, None] = None


class UserInDB(User):
    """_summary_

    Args:
        User (_type_): _description_
    """
    hashed_password: str


class UserLogin(BaseModel):
    """_summary_

    Args:
        BaseModel (_type_): _description_
    """
    username: Union[str, None] = None
    hashed_password: Union[str, None] = None

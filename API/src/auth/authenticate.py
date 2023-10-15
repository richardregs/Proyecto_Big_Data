"""
Authenticate
"""

from fastapi import HTTPException
from passlib.context import CryptContext

from model.User import UserInDB


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "dmc": {
        "username": "dmc",
        "full_name": "dmc",
        "email": "dmc@example.com",
        "disabled": False,
        "hashed_password":
        "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
    }
}


def get_user(username):
    """_summary_

    Args:
        username (_type_): _description_

    Returns:
        _type_: _description_
    """
    db = fake_users_db
    if username in db:
        user_data = db[username]
        return UserInDB(**user_data)
    return None


def authenticate_user(username, password):
    """_summary_

    Args:
        username (_type_): _description_
        password (_type_): _description_

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    user = get_user(username)

    if user is None or user.username is None:
        raise HTTPException(status_code=401,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})

    if not verify_password(password, user.hashed_password):
        raise HTTPException(status_code=401,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


def verify_password(password, hashed_password):
    """_summary_

    Args:
        password (_type_): _description_
        hashed_password (bool): _description_

    Returns:
        _type_: _description_
    """
    return pwd_context.verify(password, hashed_password)

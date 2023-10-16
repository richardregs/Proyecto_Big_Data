"""
Token
"""
from typing import Union
from datetime import datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
from fastapi import HTTPException, Depends
from jose import jwt, JWTError, exceptions

from auth.authenticate import get_user
from model.User import User


ouath2_schema = OAuth2PasswordBearer("/token")

SECRET_KEY = "4e077aec99672bae373cfc08783672223e917b793d5076b47722be2c98388816"
ALGORITHM = "HS256"


def create_token(data: dict, time_expire: Union[datetime, None] = None):
    """_summary_

    Args:
        data (dict): _description_
        time_expire (Union[datetime, None], optional): . Defaults to None.

    Returns:
        _type_: _description_
    """
    data_copy = data.copy()
    if time_expire is None:
        expires = datetime.utcnow() + timedelta(minutes=120)
    else:
        expires = datetime.utcnow() + time_expire

    data_copy.update({"exp": expires})
    token_jwt = jwt.encode(data_copy, key=SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt


def validate_token(token, output=False):
    """_summary_

    Args:
        token (_type_): _description_
        output (bool, optional): _description_. Defaults to False.

    Returns:
        _type_: _description_
    """
    try:
        if output:
            return jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
        jwt.decode(token, key=SECRET_KEY, algorithms=[ALGORITHM])
    except exceptions.ExpiredSignatureError:
        return JSONResponse(content={"message": "Token Expired"},
                            status_code=401)
    except exceptions.JWTError:
        return JSONResponse(content={"message": "Error with token JWT"},
                            status_code=401)


def get_user_current(token: str = Depends(ouath2_schema)):
    """_summary_

    Args:
        token (str, optional): . Defaults to Depends(ouath2_schema).

    Raises:
        HTTPException: _description_
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    try:
        token_decode = jwt.decode(token, key=SECRET_KEY, algorithms=ALGORITHM)
        username = token_decode.get("sub")
        if username is None:
            raise HTTPException(status_code=401,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
    except JWTError:
        username = ""

    user = get_user(username)
    if not user:
        raise HTTPException(status_code=401,
                            detail="Could not validate credentials",
                            headers={"WWW-Authenticate": "Bearer"})
    return user


def get_user_disabled_current(user: User = Depends(get_user_current)):
    """_summary_

    Args:
        user (User, optional): . Defaults to Depends(get_user_current).

    Raises:
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    if not user.disabled:
        raise HTTPException(status_code=400, detail="Inactive User")
    return user

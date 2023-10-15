""" FastAPI main file
This file contains the FastAPI app and the endpoints:
    - Report 1: post data in "/data/bigdata/raw"
    - Report 2: reply files in "/data/bigdata/raw"
"""

# Third party imports
import os
from dotenv import load_dotenv

from fastapi import FastAPI, Header

from auth.authenticate import authenticate_user
from auth.token import create_token, validate_token
from model.User import UserLogin
from routes.routes_files import files_routes

load_dotenv()
PATH_API = os.getenv('PATH_API')

app = FastAPI()
app.include_router(files_routes, prefix=PATH_API)


@app.get("/")
def index():
    """
    Index
    Returns: Hi World
    """
    return {"Index": "Hi World"}


@app.post("/user")
def user_login(user_token: UserLogin):
    """
    Index
    Returns: user
    """
    user_db = authenticate_user(user_token.username,
                                user_token.hashed_password)
    access_token_jwt = create_token({"sub": user_db.username})
    return {"access_token": access_token_jwt,
            "token_type": "bearer"}


@app.post("/verify/token")
def verify_token(Authorization: str = Header(None)):
    """_summary_

    Args:
        Authorization (str, optional): _description_. Defaults to Header(None).

    Returns:
        _type_: _description_
    """
    token = Authorization.split(" ")[1]
    return validate_token(token, output=True)

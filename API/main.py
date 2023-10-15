""" FastAPI main file
This file contains the FastAPI app and the endpoints:
    - Report 1: post data in "/data/bigdata/raw"
    - Report 2: reply files in "/data/bigdata/raw"
"""

# Third party imports
import os
from typing import Dict
from datetime import timedelta
from dotenv import load_dotenv

from fastapi import FastAPI, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

import pandas as pd
from auth.authenticate import authenticate_user
from auth.token import create_token, get_user_disabled_current
from model.User import User
from utils.gcs_actions import ls_bucket, upload_file

load_dotenv()
app = FastAPI()

PATH_API = os.getenv('PATH_API')
PATH_DIR = os.getenv('PATH_DIR')

ouath2_schema = OAuth2PasswordBearer("/token")

@app.get("/")
def index():
    """
    Index
    Returns: Hi World
    """
    return {"Index": "Hi World"}


@app.get("/user/me")
def user(user_me: User = Depends(get_user_disabled_current)):
    """_summary_

    Args:
        user (User, optional):
        . Defaults to Depends(get_user_disabled_current).

    Returns:
        _type_: _description_
    """
    return user_me


@app.post("/token")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """_summary_

    Args:
        form_data (OAuth2PasswordRequestForm, optional):
        . Defaults to Depends().

    Returns:
        _type_: _description_
    """
    user_form = authenticate_user(form_data.username, form_data.password)
    access_token_expires = timedelta(minutes=30)
    access_token_jwt = create_token({"sub": user_form.username},
                                    access_token_expires)
    return {"access_token": access_token_jwt,
            "token_type": "bearer"}


@app.get(path=PATH_API)
async def get_files():
    """Get method

    Returns:
        list: list of files
    """
    response_dict = {}
    status_code = 404

    try:
        file_list = ls_bucket()
        response_dict = {
            "service": "get_files",
            "files": file_list
        }
        status_code = 200
        return JSONResponse(content=response_dict, status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)


@app.post(path=PATH_API)
async def create_file(body: Dict):
    """"
    body: {
        "file_name": {str},
        "data": {json}
        }
    """
    response_dict = {}
    status_code = 404
    try:
        file_name = body["file_name"]
        file_list = ls_bucket()
        for file in file_list:
            if f"{file_name}.csv" in file:
                status_code = 201
                return JSONResponse(content="the file exists",
                                    status_code=status_code)
        response_dict = body["data"]
        upload_file(f"{file_name}.csv", response_dict)
        status_code = 200
        return JSONResponse(content="ok", status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)


@app.put(path=PATH_API)
async def replace_file(body: Dict):
    """"
    body: {
        "file_name": {str},
        "data": {json}
        }
    """
    response_dict = {}
    status_code = 404
    try:
        file_name = body["file_name"]
        file_list = ls_bucket()
        for file in file_list:
            if f"{file_name}.csv" not in file:
                return JSONResponse(content="Not found file",
                                    status_code=status_code)
        response_dict = body["data"]
        upload_file(f"{file_name}.csv", response_dict)
        status_code = 200
        return JSONResponse(content="ok", status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)

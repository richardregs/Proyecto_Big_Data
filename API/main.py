""" FastAPI main file
This file contains the FastAPI app and the endpoints:
    - Report 1: post data in "/data/bigdata/raw"
    - Report 2: reply files in "/data/bigdata/raw"
"""

# Third party imports
import os
from typing import Dict
from dotenv import load_dotenv

from fastapi import FastAPI
from fastapi.responses import JSONResponse

import pandas as pd
# import uvicorn # Comment for deploy

load_dotenv()
app = FastAPI()

PATH_API = os.getenv('PATH_API')
PATH_DIR = os.getenv('PATH_DIR')


@app.get(path=PATH_API)
async def get_files():
    """Get method

    Returns:
        list: list of files
    """
    response_dict = {}
    status_code = 404

    try:
        file_list = os.listdir(PATH_DIR)
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
        path_file = os.path.join(PATH_DIR, f"{file_name}.csv")
        file_list = os.listdir(PATH_DIR)
        if f"{file_name}.csv" in file_list:
            status_code = 201
            return JSONResponse(content="the file exists",
                                status_code=status_code)
        response_dict = body["data"]
        df = pd.DataFrame(response_dict)
        df.to_csv(path_file, index=False)
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
    response_dict = dict()
    status_code = 404
    try:
        file_name = body["file_name"]
        path_file = os.path.join(PATH_DIR, f"{file_name}.csv")
        file_list = os.listdir(PATH_DIR)
        if f"{file_name}.csv" not in file_list:
            return JSONResponse(content="Not found file",
                                status_code=status_code)
        response_dict = body["data"]
        df = pd.DataFrame(response_dict)
        df.to_csv(path_file, index=False)
        status_code = 200
        return JSONResponse(content="ok", status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)

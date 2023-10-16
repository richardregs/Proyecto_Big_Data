from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from middleware.verify_token_route import VerifyTokenRoute
from utils.gcs_actions import ls_bucket, upload_file

files_routes = APIRouter(route_class=VerifyTokenRoute)


@files_routes.post("/users")
def users(name: str):
    """_summary_

    Args:
        name (str): _description_

    Returns:
        _type_: _description_
    """
    return {f"{name}"}


@files_routes.get(path='/')
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


@files_routes.post(path='/')
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
        response_dict = str(body["data"])
        upload_file(f"{file_name}.csv", response_dict)
        status_code = 200
        return JSONResponse(content="ok", status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)


@files_routes.put(path='/')
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
        file_exist = False
        for file in file_list:
            if f"{file_name}.csv" in file:
                file_exist = True
                break
        if not file_exist:
            return JSONResponse(content="Not found file",
                                status_code=status_code)
        response_dict = str(body["data"])
        upload_file(f"{file_name}.csv", response_dict)
        status_code = 200
        return JSONResponse(content="ok", status_code=status_code)
    except Exception as err:
        return JSONResponse(content=err, status_code=status_code)

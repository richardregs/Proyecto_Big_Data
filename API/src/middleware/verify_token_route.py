"""
Verify tokens
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute
from auth.token import validate_token


class VerifyTokenRoute(APIRoute):
    """
    Verify class
    """
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            try:
                token = request.headers["Authorization"].split(" ")[1]
            except KeyError:
                return JSONResponse(content={"message":
                                             "No valid token found"},
                                    status_code=401)
            validation_response = validate_token(token, output=False)

            if validation_response is None:
                return await original_route(request)
            return validation_response

        return verify_token_middleware

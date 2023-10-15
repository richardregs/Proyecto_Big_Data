"""
Verify tokens
"""
from fastapi import Request
from fastapi.routing import APIRoute
from auth.token import validate_token


class VerifyTokenRoute(APIRoute):
    """
    Verify class
    """
    def get_route_handler(self):
        original_route = super().get_route_handler()

        async def verify_token_middleware(request: Request):
            token = request.headers["Authorization"].split(" ")[1]
            validation_response = validate_token(token, output=False)

            if validation_response is None:
                return await original_route(request)
            else:
                return validation_response

        return verify_token_middleware

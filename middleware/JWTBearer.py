import typing

from strawberry.permission import BasePermission
from strawberry.types import Info
from strawberry.exceptions import StrawberryGraphQLError

from middleware.JWTManager import JWTManager


class UnauthorizedException(StrawberryGraphQLError):
    ...


class IsAuthenticated(BasePermission):
    message = "User is not authenticated!"
    error_class = UnauthorizedException
    error_extensions = {"code": "UNAUTHORIZED"}

    def has_permission(
        self, source: typing.Any, info: Info, **kwargs: typing.Any
    ) -> bool:
        request = info.context["request"]

        authentication: str = request.headers.get("authentication")

        try:
            if authentication:
                token = authentication.split("Bearer ")[-1]
                return JWTManager.verify_jwt(token)
        except Exception as e:
            self.message = str(e)
            print(e)

        return False

import logging

from passlib.context import CryptContext

from models.user import User
from repository.user import UserRepository
from schema import RegisterInput, LoginInput, LoginType, ServiceReturnType
from middleware.JWTManager import JWTManager


# Silences warnings in new version of bcrypt
# https://github.com/pyca/bcrypt/issues/684
logging.getLogger("passlib").setLevel(logging.ERROR)


class AuthenticationService:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @staticmethod
    async def login(login_data: LoginInput):
        # check existing user
        existing_user = await UserRepository.get_by_email(login_data.email)

        if not existing_user:
            raise ValueError("Email not found!")

        if not AuthenticationService.pwd_context.verify(
            login_data.password, existing_user.password
        ):
            raise ValueError("Wrong password!")

        token = JWTManager.generate_token({"sub": existing_user.email})

        return LoginType(email=existing_user.email, token=token)

    @staticmethod
    async def register(user_data: RegisterInput):
        existing_user = await UserRepository.get_by_email(user_data.email)

        if existing_user:
            raise ValueError("Email already exists!")

        user = User(
            id=None,
            email=user_data.email,
            name=user_data.name,
            password=AuthenticationService.pwd_context.hash(user_data.password),
        )

        user = await UserRepository.create(user)

        if user:
            return ServiceReturnType(
                success=True, message=f"User {user_data.email} created successfully."
            )
        else:
            return ServiceReturnType(
                success=False, message=f"Failed to create user {user_data.email}."
            )

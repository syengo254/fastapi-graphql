import os
from typing import Optional
from datetime import datetime, timedelta

from jose import jwt

from dotenv import load_dotenv

# load .env vars
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "mysecret")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))


class JWTManager:
    @staticmethod
    def generate_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()

        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

        to_encode.update({"exp": expire})
        encode_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

        return encode_jwt

    @staticmethod
    def verify_jwt(token: str):
        try:
            decode_token = jwt.decode(token=token, key=SECRET_KEY, algorithms=[ALGORITHM])
            current_timestamp = datetime.utcnow().timestamp()

            if not decode_token:
                raise ValueError("Invalid token!")
            elif decode_token["exp"] <= current_timestamp:
                raise ValueError("Token expired!")
            return True
        except ValueError as e:
            print(e)
            return False

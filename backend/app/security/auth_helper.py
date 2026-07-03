import jwt
import time
import asyncio  
from uuid import UUID
from pwdlib import PasswordHash
from decouple import config
from fastapi import HTTPException

JWT_SECRET = config("JWT_SECRET")
JWT_ALGO = config("JWT_ALGO")

class AuthHandler(object):
    @staticmethod
    def sign_jwt(user_id: UUID):
        payload = {
            "user_id": str(user_id),
            "expires": time.time() + 900
        }

        token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGO)

        return token

    @staticmethod
    def decode_jwt(token: str):
        try:
            decoded_token= jwt.decode(token, JWT_SECRET, algorithms=JWT_ALGO)

            return decoded_token
        
        except Exception as e:
            raise HTTPException(status_code = 500, detail = f"Couldn't decode the token: {e}")

class HashHelper(object):

    _hasher = PasswordHash.recommended()

    @staticmethod
    async def hash_password(password: str) -> str:
        if not password:
            raise ValueError("Password cannot be empty.")

        return await asyncio.to_thread(HashHelper._hasher.hash, password)  


    @staticmethod
    async def verify_password(plain_password: str, hashed_password:str) -> bool:
        if not plain_password or not hashed_password:
            return False

        try:
            return await asyncio.to_thread(HashHelper._hasher.verify, plain_password, hashed_password)  
        except Exception:
            return False
from app.db.repository import UserRepository
from app.db.schemas.users import UserSignup, UserLogin, UserWithToken
from app.security.auth_helper import HashHelper, AuthHandler
from sqlalchemy.ext.asyncio import AsyncSession 
from fastapi import HTTPException
from app.db.models.users import User
from datetime import timezone, datetime
from uuid import UUID

class UserService:
    def __init__(self, session: AsyncSession):  
        self.__UserRepository = UserRepository(session)

    async def signup(self, user_details: UserSignup):  # Corrected from "def signup(...)" to "async def signup(...)"
        if bool(await self.__UserRepository.get_user_by_email_username(username_email=user_details.email)) or \
            bool(await self.__UserRepository.get_user_by_email_username(username_email=user_details.username)):  # Corrected from "bool(self.__UserRepository.get_user_by_email_username(...))" to "bool(await self.__UserRepository.get_user_by_email_username(...))"
            raise HTTPException(status_code = 400, detail = "Username or email already in use. Please login.")

        hashed_password = await HashHelper.hash_password(password=user_details.password)  # Corrected from "hashed_password = HashHelper.hash_password(...)" - HashHelper.hash_password is async and was never awaited, so hashed_password held a coroutine, not a string
        user_details.password = hashed_password

        return await self.__UserRepository.create_user(user_data=user_details)  # Corrected from "return self.__UserRepository.create_user(...)" to "return await self.__UserRepository.create_user(...)"

    async def login(self, login_details: UserLogin):  # Corrected from "def login(...)" to "async def login(...)"
        user: User = await self.__UserRepository.get_user_by_email_username(login_details.username_email)  # Corrected from "user: User = self.__UserRepository.get_user_by_email_username(...)" to "... = await ..."
        if not user:
            raise HTTPException(status_code=401, detail = "No user found. Please create an account")

        if user.locked_until is not None and user.locked_until > datetime.now(timezone.utc):
            raise HTTPException(status_code=402, detail = f"Please try after: {user.locked_until}")

        if not user.is_active:
            ...
            
        if await HashHelper.verify_password(plain_password=login_details.password, hashed_password=user.password):  # Corrected from "if HashHelper.verify_password(...)" - was async but unawaited, so the coroutine object (always truthy) was tested instead of the real bool
            token = AuthHandler.sign_jwt(user_id=user.user_id)
            if token:
                await self.__UserRepository.update_last_login(user=user)  # Corrected from "self.__UserRepository.update_last_login(user=user)" to "await self.__UserRepository.update_last_login(user=user)"
                return UserWithToken(token=token)

            raise HTTPException(status_code=500, detail="Unable to process request.")

        await self.__UserRepository.increased_failed_attempts(user=user)  # Corrected from "self.__UserRepository.icrease_failed" (typo'd, unawaited, unreachable) to "await self.__UserRepository.increased_failed_attempts(user=user)"
        raise HTTPException(status_code=401, detail="Invalid credentials.")

    async def get_user_by_id(self, user_id: UUID) -> User | None:
        user = await self.__UserRepository.get_user_by_id(id=user_id)

        if user:
            return user

        raise HTTPException(status_code = 400, detail = "User not found!")

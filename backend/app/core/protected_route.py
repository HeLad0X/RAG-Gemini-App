from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from app.security.auth_helper import AuthHandler
from app.service.users import UserService
from app.db.database import get_db
from app.db.schemas.users import UserOutput
from app.db.models.users import User

async def get_current_user( 
    session: AsyncSession = Depends(get_db),
    authorization: Annotated[str | None, Header(alias="authorization")] = None) -> UserOutput:

    auth_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Invalid Authentication Credentials"
    )

    if not authorization:
        raise auth_exception

    payload = AuthHandler.decode_jwt(token=authorization)
    if payload and payload["user_id"]:
        try:
            user: User = await UserService(session=session).get_user_by_id(payload["user_id"])

            return UserOutput(
                username=user.username,
                email = user.email,
                user_id = (user.user_id),
                first_name = user.first_name,
                last_name = user.last_name,
                is_active = user.is_active,
                is_verified = user.is_verified,
                failed_login_attempts = user.failed_login_attempts
            )
        except Exception as error:
            raise error

    raise auth_exception
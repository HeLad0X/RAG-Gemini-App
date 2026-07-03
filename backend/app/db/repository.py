from sqlalchemy import select 
from sqlalchemy.ext.asyncio import AsyncSession 
from app.db.schemas.users import UserSignup
from app.db.models.users import User
from uuid import UUID
from datetime import timedelta, timezone, datetime

class BaseRepository:
    def __init__(self, session: AsyncSession) -> None:  
        self.session = session


class UserRepository(BaseRepository):
    async def create_user(self, user_data: UserSignup):  
        newUser = User(**user_data.model_dump(exclude_none=True))

        try:
            self.session.add(instance=newUser)
            await self.session.commit()  
            await self.session.refresh(instance=newUser)  

            return newUser
        except Exception as e:
            return {"Exception": e}

    async def get_user_by_email_username(self, username_email) -> User | None: 
        result = await self.session.execute(select(User).filter_by(email = username_email)) 
        user = result.scalar_one_or_none()

        if not bool(user):
            result = await self.session.execute(select(User).filter_by(username = username_email)) 
            user = result.scalar_one_or_none()

        return user

    async def get_user_by_id(self, id) -> User | None:  
        result = await self.session.execute(select(User).filter_by(user_id = UUID(id)))  
        user = result.scalar_one_or_none()

        return user

    async def update_last_login(self, user: User):  
        user.failed_login_attempts = 0
        user.last_login_at = datetime.now(timezone.utc)
        user.locked_until = None

        await self.session.commit()  

    async def increased_failed_attempts(self, user: User):  
        user.failed_login_attempts += 1

        if user.failed_login_attempts > 5:
            user.locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)

        await self.session.commit()  

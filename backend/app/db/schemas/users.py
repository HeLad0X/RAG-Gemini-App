from pydantic import EmailStr, BaseModel
from uuid import UUID

class UserSignup(BaseModel):
    username: str
    email: EmailStr
    password: str
    first_name: str
    last_name: str

class UserLogin(BaseModel):
    username_email: str | EmailStr
    password: str


class UserWithToken(BaseModel):
    token: str

class UserOutput(BaseModel):
    username: str
    email: str
    user_id: UUID
    first_name: str
    last_name: str
    is_active: bool
    is_verified: bool
    failed_login_attempts: int
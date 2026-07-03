from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import APIRouter, Depends, HTTPException, status
from app.db.schemas.users import UserLogin, UserSignup, UserWithToken, UserOutput
from app.db.database import get_db
from app.service.users import UserService

auth_router = APIRouter()

@auth_router.post("/login", status_code=200, response_model=UserWithToken)
async def login(login_details: UserLogin, session: AsyncSession = Depends(get_db)):
    try:
        return await UserService(session=session).login(login_details=login_details)
    
    except HTTPException:
        raise
        
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to login to your account: {str(error)}"
        )


@auth_router.post("/signup", status_code=201, response_model=UserOutput)
async def signup(signup_details: UserSignup, session: AsyncSession = Depends(get_db)):
    try: 
        return await UserService(session=session).signup(user_details=signup_details)
    except HTTPException:
        raise
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to create your account: {str(error)}"
        )
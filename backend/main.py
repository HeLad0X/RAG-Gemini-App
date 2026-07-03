from fastapi import FastAPI, Depends, status
from app.routers.auth import auth_router
from app.db.schemas.users import UserOutput
from app.core.protected_route import get_current_user
from fastapi.responses import RedirectResponse
import uvicorn



app = FastAPI()
app.include_router(router=auth_router, tags=["auth"], prefix="/rag-app/v1/auth")

@app.get("/rag-app/v1/me")
async def me(user: UserOutput = Depends(get_current_user)):
    return {"data": user}

@app.get("/")
async def home():
    return RedirectResponse(
        url="/rag-app/v1/me",
        status_code = status.HTTP_302_FOUND
    )

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)
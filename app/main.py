from datetime import datetime, timedelta, timezone
import os
from typing import Annotated, List

from dependencies import get_user_repository
import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.settings import APP_VERSION, APP_NAME, ACCESS_TOKEN_EXPIRE_MINUTES 
from schemas import User, Token, TokenData, UserCreate
from app.security import verify_password, DUMMY_HASH
from app.auth import authenticate_user, create_access_token, get_current_user, oauth2_scheme
from api.v1 import router as v1_router



app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION
)

# Routers
app.include_router(v1_router.router, prefix="/api")

@app.post("/login")
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], repo=Depends(get_user_repository)
) -> Token:
    user = authenticate_user(repo, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"iss": "stead-watch", "sub": user.username, "role": user.role, 'iat': datetime.now(timezone.utc)}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@app.post("/create-user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, repo=Depends(get_user_repository)):
    if repo.exists(user.username):
        raise HTTPException(status_code=400, detail="User with this username already exists")
    try:
        new_user = repo.create(user)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
    return new_user

@app.get("/users/me")
async def read_users_me(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
# Health check
@app.get("/health")
def health():
    return {"status": "ok"}


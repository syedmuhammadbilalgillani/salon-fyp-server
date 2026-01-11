from fastapi import APIRouter, HTTPException
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.services.auth_service import register_user, login_user

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=dict)
async def register(data: UserCreate):
    user = await register_user(
        name=data.name,
        email=data.email,
        password=data.password,
        phone=data.phone,
        role=data.role
    )
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}

@router.post("/login")
async def login(data: UserLogin):
    token = await login_user(data.email, data.password)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
from app.database import user_collection
from app.utils.password import hash_password, verify_password
from app.services.jwt_service import create_access_token
from app.schemas.user_schema import UserRole

async def register_user(name: str, email: str, password: str, phone: str, role: UserRole, otp: Optional[str] = None):
    existing = await user_collection.find_one({"email": email})
    if existing:
        return None

    user = {
        "name": name,
        "email": email,
        "password": hash_password(password),
        "phone": phone,
        "role": role.value,
        "otp": otp,
        "is_verified": False  # You may want to track OTP verification
    }
    await user_collection.insert_one(user)
    return user

async def login_user(email: str, password: str):
    user = await user_collection.find_one({"email": email})
    if not user or not verify_password(password, user["password"]):
        return None

    token = create_access_token({"sub": user["email"], "role": user.get("role")})
    return token
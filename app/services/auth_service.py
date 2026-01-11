from typing import Optional
from bson import ObjectId
from app.database import user_collection
from app.utils.password import hash_password, verify_password
from app.services.jwt_service import create_access_token
from app.schemas.user_schema import UserRole

def user_to_dict(user_doc: dict) -> dict:
    """Convert MongoDB user document to JSON-serializable dict"""
    if not user_doc:
        return None
    
    user_dict = {
        "id": str(user_doc["_id"]),  # Convert ObjectId to string
        "name": user_doc.get("name"),
        "email": user_doc.get("email"),
        "phone": user_doc.get("phone"),
        "role": user_doc.get("role"),
        "is_verified": user_doc.get("is_verified", False),
    }
    
    # Optionally include OTP if needed
    if "otp" in user_doc:
        user_dict["otp"] = user_doc["otp"]
    
    return user_dict

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

async def login_user(email: str, password: str, userType: UserRole):
    print(email, password, userType.value,"email, password, userType")
    user = await user_collection.find_one({"email": email, "role": userType.value})
    print(user,"user")
    if not user or not verify_password(password, user["password"]):
        return None

    token = create_access_token({"sub": user["email"], "role": user.get("role")})
    # Convert MongoDB document to JSON-serializable dict (excludes password)
    user_dict = user_to_dict(user)
    return {"token": token, "user": user_dict}
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies.db import Get_db
from dependencies.redis import Get_redis
from models.services import Services
from api.services.auth import (
    create_access_token,
    get_password_hash,
    verify_password,
)
from datetime import timedelta
from pydantic import BaseModel

from fastapi.responses import JSONResponse

router = APIRouter()


class LoginRequest(BaseModel):
    owner: str
    password: str


class ResetPasswordRequest(BaseModel):
    owner: str
    old_password: str
    new_password: str


@router.post("/register")
async def register_service(register_data: LoginRequest, db: Session = Depends(Get_db)):
    owner = register_data.owner
    password = register_data.password
    """Register a new service with owner and password"""
    if db.query(Services).filter(Services.owner == owner).first():
        raise HTTPException(
            status_code=400, detail="Owner already registered"
        )

    # Hash the password
    hashed_password = get_password_hash(password)

    # Create new service
    service = Services(owner=owner, password=hashed_password)

    db.add(service)
    db.commit()
    db.refresh(service)

    return {
        "owner": service.owner,
        "owner_id": service.id,  # Add this line
        "message": "Registration successful",
    }


@router.post("/login")
async def login_service(
    login_data: LoginRequest,
    db: Session = Depends(Get_db),
    redis_client=Depends(Get_redis),
):
    """Login with owner and password"""
    service = db.query(Services).filter(Services.owner == login_data.owner).first()

    if not service or not verify_password(login_data.password, service.password):
        return JSONResponse(status_code=401, content="Incorrect user or password")
    
    # Invalidate all existing tokens for this user
    for key in redis_client.scan_iter(f"token:*"):
        if redis_client.get(key) == service.owner:
            redis_client.delete(key)

    # Generate access token
    access_token = create_access_token(
        data={"sub": service.owner}, redis_client=redis_client
    )

    return {"access_token": access_token, "token_type": "Bearer"}


@router.post("/reset-password")
async def reset_password(
    reset_data: ResetPasswordRequest,
    db: Session = Depends(Get_db),
    redis_client=Depends(Get_redis),
):
    """Reset password with old password verification"""
    service = db.query(Services).filter(Services.owner == reset_data.owner).first()
    if not service or not verify_password(reset_data.old_password, service.password):
        return JSONResponse(status_code=401, content="Incorrect password")

    # Update password
    service.password = get_password_hash(reset_data.new_password)
    db.commit()

    # Invalidate all existing tokens for this user
    for key in redis_client.scan_iter(f"token:*"):
        if redis_client.get(key) == service.owner:
            redis_client.delete(key)

    return {"message": "Password reset successful"}


@router.post("/validate-token")
async def validate_token(token: str, redis_client=Depends(Get_redis)):
    """Validate token against Redis storage"""
    if redis_client.exists(f"token:{token}"):
        return {"valid": True}
    return {"valid": False}


# @router.post("/logout")
# async def logout(token: str = Depends(oauth2_scheme)):
#     """Logout by invalidating the token"""
#     redis_client.delete(f"token:{token}")
#     return {"message": "Successfully logged out"}

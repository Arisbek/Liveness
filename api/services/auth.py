from datetime import datetime, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from api.services.jwt.jwt_service import jwt_decode_data, jwt_encode_data
from dependencies.db import Get_db
from dependencies.redis import Get_redis
from models.services import Services

from fastapi.responses import JSONResponse

from typing import Annotated

ACCESS_TOKEN_EXPIRE_MINUTES = 3000

# Setup password hashing and OAuth2
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def create_access_token(
    data: dict,
    redis_client=Depends(Get_redis),
) -> str:
    expire = datetime.now() + (
        timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    data["exp"] = expire
    encoded_jwt = jwt_encode_data(data)
    # Store token in Redis with expiration
    # print(isinstance(data["sub"],str))
    redis_client.set(
        f"token:{encoded_jwt}",
        str(data["sub"]),  # Store the owner identifier
    )
    redis_client.expire(
        f"token:{encoded_jwt}",
        60*ACCESS_TOKEN_EXPIRE_MINUTES,  # Set expiration time
    )
    return encoded_jwt


async def get_current_service(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Session = Depends(Get_db),
    redis_client=Depends(Get_redis),
):
    try:
        owner = redis_client.get(f"token:{token}")
        # print(payload)
        # if redis_client.getex(payload):
        #     raise HTTPException(status_code=401, detail="Authorization failed")
        # print(f"Decoded payload: {payload}")
        # owner = payload.get("sub")
        print(f"Owner: {owner}")
        if owner is None:
            raise HTTPException(status_code=401, detail="User not found")
        # owner = int(owner)
    except Exception as e:
        print(f"JWTError: {e}")
        raise HTTPException(status_code=401, detail="Authorization failed")
    

    service = db.query(Services).filter(Services.owner == owner).first()
    if service is None:
        raise HTTPException(status_code=401, detail="User not found")

    return service.id

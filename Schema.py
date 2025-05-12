from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import JSON
from typing import Optional, Dict

class LogBase(BaseModel):
    time_created: datetime
    method:str
    url:str
    ip_address:str
    owner_id:int
    request: str
    response: str

    class Config:
        orm_mode = True


class CreateLog(LogBase):
    class Config:
        orm_mode = True

class ServiceBase(BaseModel):
    owner: str
    password: str

    class Config:
        orm_mode = True


class CreateService(ServiceBase):
    class Config:
        orm_mode = True

class FrameBase(BaseModel):
    owner_id: int
    frame: str
    time_created: datetime
    predictions: Optional[Dict] 

    class Config:
        orm_mode = True


class CreateFrame(FrameBase):
    class Config:
        orm_mode = True
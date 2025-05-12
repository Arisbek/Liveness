from typing import List
from fastapi import HTTPException, Depends, Request, APIRouter
from sqlalchemy.orm import Session
from models.logs import Logs
import Schema
from dependencies.db import Get_db

from .. import pagination as p

router = APIRouter()

@router.get('/', response_model=List[Schema.CreateLog])
async def test_services(pagination: p.Pagination = Depends(p.paginationParams), db: Session = Depends(Get_db)):

    offset = (pagination.page - 1) * pagination.perPage 
    logs = db.query(Logs).offset(offset).limit(pagination.perPage).all() 
    return logs
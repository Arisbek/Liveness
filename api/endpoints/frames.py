from typing import List
from fastapi import HTTPException, Depends, Request, APIRouter, Query
from sqlalchemy.orm import Session
from models.frames import Frames
import Schema
from dependencies.db import Get_db
from datetime import datetime
from .. import pagination as p

router = APIRouter()

# @router.get('/', response_model=List[Schema.CreateFrame])
# async def test_services(pagination: p.Pagination = Depends(p.paginationParams), db: Session = Depends(get_db)):

#     offset = (pagination.page - 1) * pagination.perPage 
#     frames = db.query(Frames).offset(offset).limit(pagination.perPage).all() 
#     return frames


router = APIRouter()

@router.get('/', response_model=List[Schema.CreateFrame])
async def test_services(
    pagination: p.Pagination = Depends(p.paginationParams),
    db: Session = Depends(Get_db),
    owner_id: int = Query(None, description="Filter by owner ID"),
    after: datetime = Query(None, description="Filter frames created after this time"),
    before: datetime = Query(None, description="Filter frames created before this time")
):
    offset = (pagination.page - 1) * pagination.perPage
    query = db.query(Frames)

    if owner_id:
        query = query.filter(Frames.owner_id == owner_id)
    if after:
        query = query.filter(Frames.time_created >= after)
    if before:
        query = query.filter(Frames.time_created <= before)

    frames = query.offset(offset).limit(pagination.perPage).all()
    return frames

from pydantic import BaseModel
from fastapi import Query

class Pagination(BaseModel):
    perPage: int
    page: int

def paginationParams(
        page: int = Query(ge=1, required=False, default=1,le=500000),
        perPage: int = Query(ge=1, required=False, default=1,le=500000)
        ):
    return Pagination(perPage=perPage,page=page)
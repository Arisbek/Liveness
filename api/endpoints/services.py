from typing import List
from fastapi import HTTPException, Depends, Request, APIRouter
from sqlalchemy.orm import Session
from starlette import status
from models.services import Services
import Schema
from dependencies.db import Get_db

from .. import pagination as p

router = APIRouter()

@router.get('/', response_model=List[Schema.CreateService])
async def test_services(pagination: p.Pagination = Depends(p.paginationParams), db: Session = Depends(Get_db)):

    offset = (pagination.page - 1) * pagination.perPage 
    services = db.query(Services).offset(offset).limit(pagination.perPage).all() 
    return services

# @router.post('/', status_code=status.HTTP_201_CREATED, response_model=List[Schema.CreateService])
# async def test_services_sent(request: Request, db:Session = Depends(get_db)):
#     data = await request.json()
#     owner = data.get("owner")

#     enc = jwt.encode(
#         {
#             "sub": owner,
#             "custom_payload_key": "custom payload value",
#             # token generation time
#             "iat": int(time.time()),
#         },
#         private_key,
#         algorithm="RS256",
#         # the kid ("key identifier") may not be required
#         headers={"alg": "RS256", "typ": "JWT"},
#     )
#     new_service = services.Services(owner=owner, token=enc)
#     db.add(new_service)
#     db.commit()
#     db.refresh(new_service)

#     return [new_service]


# @router.get('/{id}', response_model=Schema.CreateService, status_code=status.HTTP_200_OK)
# def get_test_one_service(id:int ,db:Session = Depends(get_db)):

#     idv_service = db.query(services.Services).filter(services.Services.id == id).first()

#     if idv_service is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"The id: {id} you requested for does not exist")
#     return idv_service

# @router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
# def delete_test_service(id:int, db:Session = Depends(get_db)):

#     deleted_service = db.query(services.Services).filter(services.Services.id == id)


#     if deleted_service.first() is None:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
#                             detail=f"The id: {id} you requested for does not exist")
#     deleted_service.delete(synchronize_session=False)
#     db.commit()



# @router.put('/{id}', response_model=Schema.CreateService)
# def update_test_service(update_service:   Schema.ServiceBase, id:int, db:Session = Depends(get_db)):

#     updated_service =  db.query(services.Services).filter(services.Services.id == id)

#     if updated_service.first() is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"The id:{id} does not exist")
#     updated_service.update(update_service.dict(), synchronize_session=False)
#     db.commit()


#     return  updated_service.first()
import uvicorn
from dependencies.db import Engine, Base
from dependencies.redis import Redis_url
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from api.api import api_router
import sys
# from socket_api import socket_app
from api.middleware.logMiddleware import LogMiddleware

from fastapi.staticfiles import StaticFiles 
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
# from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv

from create_user import create_user
from exception import CustomException
from fastapi.encoders import jsonable_encoder


load_dotenv()
sys.dont_write_bytecode = True # why I put it?

app = FastAPI()


# Add LogMiddleware with Redis URL from environment
app.add_middleware(
    LogMiddleware, 
    redis_url=Redis_url
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
                                 
app.mount("/media", StaticFiles(directory="media",check_dir=False), name="media")
app.include_router(api_router, prefix="/api")
Base.metadata.create_all(bind=Engine)

create_user() # what if error here

# Обработчик ошибок (error handler) для класса CustomException 
@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"detail": exc.errors()})
    )
# app.mount("/", socket_app)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
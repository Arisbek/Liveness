from fastapi import APIRouter
from .endpoints import services
from .endpoints import check
from .endpoints import logs
from .endpoints import frames
from .endpoints import auth
from .endpoints import generate_instructions as g
# from .middleware.logMiddleware import LogMiddleware  # Import the middleware

api_router = APIRouter()

# # Define the redis_url variable
# redis_url = "redis://localhost"

# # Add the LogMiddleware to the api_router
# api_router.add_middleware(
#     LogMiddleware, 
#     redis_url=redis_url
# )

api_router.include_router(auth.router, prefix="/auth")
api_router.include_router(check.router, prefix="/check")
api_router.include_router(services.router, prefix="/services")
api_router.include_router(logs.router, prefix="/logs")
api_router.include_router(frames.router, prefix="/frames")
api_router.include_router(g.router)
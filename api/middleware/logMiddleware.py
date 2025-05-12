from fastapi import FastAPI, Request, Response, HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware
from dependencies.redis import Get_redis
from models.logs import Logs
from models.services import Services
from models.frames import Frames
from dependencies.db import SessionLocal
from redis import Redis
import json
from datetime import datetime
from typing import Optional
import traceback

from api.endpoints.auth import LoginRequest
from api.services.auth import get_current_service

from fastapi.responses import JSONResponse
import os
from exception import CustomException

class LogMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: FastAPI, redis_url: str):
        super().__init__(app)
        self.redis_client = Redis.from_url(redis_url, decode_responses=True)
    
    async def get_request_body(self, request: Request) -> Optional[str]:
        """Safely get and format request body"""
        if request.method not in ["POST", "PUT", "PATCH"]:
            return None

        try:
            body = await request.body()
            if not body:
                return None

            # Check content type
            content_type = request.headers.get('content-type', '')
            
            if 'application/json' in content_type:
                return json.dumps(json.loads(body))
            elif 'multipart/form-data' in content_type:
                return "Multipart form data"
            elif 'image' in content_type:
                return "Image data"
            else:
                return f"Binary data of type: {content_type}"
        except Exception as e:
            return f"Error parsing request body: {str(e)}"

    async def get_response_body(self, response_body: bytes) -> str:
        """Safely parse and format response body"""
        try:
            if not response_body:
                return None

            # Try to parse as JSON
            data = json.loads(response_body)
            return json.dumps(data)
        except json.JSONDecodeError:
            # Check if it's binary data
            try:
                return response_body.decode('utf-8')
            except UnicodeDecodeError:
                return "Binary response data"
        except Exception as e:
            return f"Error parsing response body: {str(e)}"

    def get_service_from_table(self, db, login_data: LoginRequest):
        try:
            service = db.query(Services).filter(Services.owner == login_data.owner).filter(Services.password == login_data.password).first()
            if not service:
                return None
            return service.id
        except Exception:
            return None
    
    async def dispatch(self, request: Request, call_next):
        db = SessionLocal()
        log_entry = None

        try:
            # Initialize log entry
            log_entry = Logs(
                method=request.method,
                url=str(request.url),
                ip_address=request.client.host,
            )

            # Store request body
            log_entry.request = await self.get_request_body(request)

            if str(request.url).endswith("api/auth/login"):
                body = await request.json()
                # login_data = LoginRequest(**body)
                service_id = self.get_service_from_table(db, body)
                if service_id:
                    log_entry.owner_id = service_id

            else:
                auth_header = request.headers.get('Authorization')

                # Get service ID from token
                if auth_header and auth_header.startswith('Bearer '):
                    token = auth_header.split(' ')[1]
                    service_id = await get_current_service(token, db, self.redis_client)
                    log_entry.owner_id = service_id
                else:
                    return JSONResponse(status_code=401, content="Token not found")

            # Generate file path and store it in request state
            time = datetime.now()
            timestamp = time.strftime('%Y%m%d%H%M%S')
            media_dir = os.path.join("media")
            if not os.path.exists(media_dir):
                raise HTTPException(status_code=404, detail="Media folder does not exist") 
            if str(request.url).endswith("api/check/frame"):
                file_path = os.path.join(media_dir, f"{timestamp}.jpeg")
                request.state.file_path = file_path
                frame_log = Frames(
                    owner_id=service_id,
                    frame=file_path,
                    time_created=time,
                    predictions=None
                )
                db.add(frame_log)
                
                db.commit()

            # Call the next middleware/endpoint
            response = await call_next(request)

            # Store response
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk

            # Parse and store response
            log_entry.response = await self.get_response_body(response_body)

            # print(log_entry.owner_id)
            
            # Create new response with the same body
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        except HTTPException as httpe:
            return JSONResponse(status_code=401, content=httpe.detail)

        except Exception as e:
            # Log the error details
            error_details = {
                "error": str(e)
            }
            
            if log_entry:
                log_entry.response = json.dumps(error_details)
            
            # Re-raise the exception after logging
            return JSONResponse(status_code=400, content=error_details)

        finally:
            if log_entry:
                try:
                    db.add(log_entry)
                    db.commit()
                except Exception as db_error:
                    # Log database error but don't raise it
                    print(f"Error saving log entry: {str(db_error)}")
                    db.rollback()
            
            db.close()
import os
from fastapi import APIRouter, UploadFile, File, Request, HTTPException, Depends
from tempfile import NamedTemporaryFile
from models.frames import Frames
from sqlalchemy.orm import Session
from dependencies.db import Get_db
import requests
import logging
import cv2
import numpy as np
from exception import CustomException

router = APIRouter()

ML_SERVICE_URL = os.environ.get("ML_SERVICE_URL")

@router.post("/frame")
async def process_frame(
    request: Request,
    file: UploadFile = File(...),
    db: Session = Depends(Get_db),
):
    try:
        if not file:
            raise HTTPException(status_code=400, detail="Image file is missing")

        # Read image content once
        image_content = await file.read()
        nparr = np.frombuffer(image_content, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if img is None:
            raise HTTPException(
                status_code=400, detail="Error decoding the image content."
            )

        # Retrieve file_path from request state
        file_path = request.state.file_path

        # Save the image content to the specified file path
        cv2.imwrite(file_path, img)
        logging.debug(f"Image successfully saved to: {file_path}")

    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        raise CustomException(detail="No file image of format JPG, JPEG, PNG found", status_code=400)

    # temp = NamedTemporaryFile(delete=False)
    try:
        # Send to ML service
        files = {"file": (file.filename, image_content, file.content_type)}
        response = requests.post(ML_SERVICE_URL, files=files)

        if response.status_code != 200:
            raise HTTPException(
                status_code=500, 
                detail=f"ML service error: {response.text}"
            )

        result = response.json()

    except Exception as e:
        logging.error(f"Error processing the file: {e}")
        return {"message": "There was an error processing the file"}
    finally:
        # os.remove(temp.name)
        logging.debug("Temporary file removed.")

    if len(result) == 1:
        result = result[0]

        frame_log = db.query(Frames).filter_by(frame=file_path).first()
        frame_log.predictions = result
        db.commit()

        valid = False
        final_accuracy = (
            result["m10"]["calc"]
            + result["mix"]
            + result["m8"]["calc"]
            + result["m6"]["calc"]
        ) / 4
        min_accuracy = min(
            result["m10"]["calc"],
            result["m8"]["calc"],
            result["m6"]["calc"],
            result["mix"],
        )
        if result["m10c"]["accuracy"] >= 0.9:
            valid = True
        else:
            final_accuracy = min_accuracy

        return {
            "accuracy": result["m10c"]["accuracy"],
            "models": {
                "m10c": result["m10c"]["accuracy"],
                "m10": result["m10"]["calc"],
                "m8": result["m8"]["calc"],
                "m6": result["m6"]["calc"],
                "mix": result["mix"]
            },
            "result": "valid" if valid else "not valid",
        }
    else:
        return {
            "message": "only one face is accepted for validation. Provided "
            + str(len(result))
            + " faces."
        }
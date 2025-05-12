from fastapi import APIRouter
from random import shuffle

router = APIRouter()

@router.get("/generate_instructions")
async def process_frame():
    instructions = shuffle(["turn right", "turn left", "turn up", "turn down"])
    return instructions

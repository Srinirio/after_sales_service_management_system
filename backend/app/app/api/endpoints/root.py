from fastapi import *
from schemas import *

router = APIRouter()

@router.get("/",response_model=Message)
async def root():
    return {"message":"Hello World"}


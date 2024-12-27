from fastapi import APIRouter, Depends, HTTPException
from app.services.ai_service import AIServiceFactory
from app.dependencies import get_current_user
from pydantic import BaseModel

router = APIRouter()

class AIRequest(BaseModel):
    service_type: str
    prompt: str

class AIResponse(BaseModel):
    result: str

@router.post("/process", response_model=AIResponse)
async def process_ai_request(
    request: AIRequest,
    current_user = Depends(get_current_user)
):
    service = AIServiceFactory.get_service(request.service_type)
    if not service:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported AI service: {request.service_type}"
        )
    
    result = await service.process_request(request.prompt)
    return AIResponse(result=result)
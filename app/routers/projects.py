from fastapi import APIRouter, Depends, HTTPException
from typing import List
from app.models.project import Project, ProjectCreate, ProjectStatus
from app.services.ai_service import AIServiceFactory
from app.database import get_supabase
from app.dependencies import get_current_user

router = APIRouter()

@router.post("/", response_model=Project)
async def create_project(
    project: ProjectCreate,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase()
    
    data = project.dict()
    data["client_id"] = current_user["id"]
    data["status"] = ProjectStatus.PENDING
    
    result = supabase.table("projects").insert(data).execute()
    return result.data[0]

@router.get("/", response_model=List[Project])
async def get_projects(current_user = Depends(get_current_user)):
    supabase = get_supabase()
    result = supabase.table("projects").select("*").eq("client_id", current_user["id"]).execute()
    return result.data

@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int,
    current_user = Depends(get_current_user)
):
    supabase = get_supabase()
    result = supabase.table("projects").select("*").eq("id", project_id).eq("client_id", current_user["id"]).execute()
    
    if not result.data:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return result.data[0]
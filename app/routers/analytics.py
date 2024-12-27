from fastapi import APIRouter, Depends
from app.dependencies import get_current_user
from app.database import get_supabase

router = APIRouter()

@router.get("/usage")
async def get_usage_analytics(current_user = Depends(get_current_user)):
    supabase = get_supabase()
    
    # Get project statistics
    projects = supabase.table("projects").select("*").eq("client_id", current_user["id"]).execute()
    
    # Calculate analytics
    total_projects = len(projects.data)
    total_cost = sum(project["cost"] for project in projects.data)
    projects_by_status = {}
    for project in projects.data:
        status = project["status"]
        projects_by_status[status] = projects_by_status.get(status, 0) + 1
    
    return {
        "total_projects": total_projects,
        "total_cost": total_cost,
        "projects_by_status": projects_by_status
    }
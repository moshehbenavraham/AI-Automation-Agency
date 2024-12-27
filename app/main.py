from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, projects, analytics, ai_services

app = FastAPI(title="AI Agency Management System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(projects.router, prefix="/projects", tags=["Projects"])
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(ai_services.router, prefix="/ai-services", tags=["AI Services"])
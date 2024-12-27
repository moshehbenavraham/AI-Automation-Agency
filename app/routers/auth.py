from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from app.models.user import UserCreate, User
from app.config import get_settings
from app.database import get_supabase

router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict):
    settings = get_settings()
    expires = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    to_encode = data.copy()
    to_encode.update({"exp": expires})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

@router.post("/register", response_model=User)
async def register(user: UserCreate):
    supabase = get_supabase()
    hashed_password = pwd_context.hash(user.password)
    
    data = {
        "email": user.email,
        "hashed_password": hashed_password,
        "company_name": user.company_name
    }
    
    result = supabase.table("users").insert(data).execute()
    return result.data[0]

@router.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    supabase = get_supabase()
    user = supabase.table("users").select("*").eq("email", form_data.username).execute()
    
    if not user.data or not pwd_context.verify(form_data.password, user.data[0]["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    access_token = create_access_token({"sub": user.data[0]["email"]})
    return {"access_token": access_token, "token_type": "bearer"}
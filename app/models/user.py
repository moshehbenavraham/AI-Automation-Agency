from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    company_name: str

class User(BaseModel):
    id: int
    email: EmailStr
    company_name: str

class UserInDB(User):
    hashed_password: str
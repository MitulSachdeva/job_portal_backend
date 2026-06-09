from typing import List, Optional
from pydantic import BaseModel

class jobBase(BaseModel):
    title: str
    description: str
    company: str
    location: str

class jobCreate(jobBase):
    pass

class jobUpdate(jobBase):
    pass

class job(jobBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

class applicationBase(BaseModel):
    job_id: int

class applicationCreate(applicationBase):
    pass

class application(applicationBase):
    id: int
    applicant_id: int
    status: str

    class Config:
        from_attributes = True

class userBase(BaseModel):
    email: str
    role: str = "seeker"

class userCreate(userBase):
    password: str

class user(userBase):
    id: int
    is_active: bool
    jobs: List[job] = []

    class Config:
        orm_mode = True

class token(BaseModel):
    access_token: str
    token_type: str

class tokenData(BaseModel):
    email: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    email: str
    role: str
    is_active: bool

    class Config:
        from_attributes = True
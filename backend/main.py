from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Optional
from fastapi.middleware.cors import CORSMiddleware
from jose import JWTError, jwt
from datetime import timedelta


import models
import schemas
import crud
import auth

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

#dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close() 
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = schemas.tokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_email(db, email=token_data.email)
    if user is None:
        raise credentials_exception
    return user

@app.post("/register", response_model=schemas.user)

def register(user: schemas.userCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token", response_model=schemas.token)

def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}    

@app.post("/jobs/", response_model=schemas.job)
def create_job(
    job: schemas.jobCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    if current_user.role != "hirer":
        raise HTTPException(
            status_code=403,
            detail="Only hirers can create jobs"
        )

    return crud.create_job(
        db=db,
        job=job,
        owner_id=current_user.id
    )

@app.post("/jobs/{job_id}/apply")
def apply_for_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    # Only seekers can apply
    if current_user.role != "seeker":
        raise HTTPException(
            status_code=403,
            detail="Only seekers can apply for jobs"
        )

    # Check if job exists
    job = db.query(models.Job).filter(
        models.Job.id == job_id
    ).first()

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    # Check if already applied
    existing_application = crud.get_applications(
        db,
        job_id,
        current_user.id
    )

    if existing_application:
        raise HTTPException(
            status_code=400,
            detail="Already applied to this job"
        )

    return crud.create_application(
        db,
        job_id,
        current_user.id
    )

@app.get("/jobs/", response_model=List[schemas.job])
def get_jobs(
    skip: int = 0,
    limit: int = 10,
    location: Optional[str] = None,
    title: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return crud.get_jobs(
        db=db,
        skip=skip,
        limit=limit,
        location=location,
        title=title
    )

@app.get("/")
def home():
    return {"message": "Job Portal API Running"}

@app.get("/me", response_model=schemas.UserResponse)
def get_me(current_user=Depends(get_current_user)):
    return current_user

@app.get("/jobs/{job_id}", response_model=schemas.job)
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    return job

@app.get("/jobs/{job_id}/applications")
def get_job_applications(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return job.applications

@app.put("/jobs/{job_id}", response_model=schemas.job)
def update_job(
    job_id: int,
    job_data: schemas.jobUpdate,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    return crud.update_job(
        db,
        job_id,
        job_data
    )

@app.delete("/jobs/{job_id}")
def delete_job(
    job_id: int,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    job = crud.get_job(db, job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if job.owner_id != current_user.id:
        raise HTTPException(
            status_code=403,
            detail="Not authorized"
        )

    crud.delete_job(db, job_id)

    return {
        "message": "Job deleted successfully"
    }
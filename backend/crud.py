from sqlalchemy.orm import Session
import models
import schemas
from auth import get_password_hash

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.userCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_jobs(db: Session, skip: int=0, limit: int=100, location: str=None, title: str=None):
    query = db.query(models.Job)
    if location:
        query = query.filter(models.Job.location.ilike(f"%{location}%"))
    if title:
        query = query.filter(models.Job.title.ilike(f"%{title}%"))
    return query.offset(skip).limit(limit).all()

def create_job(db: Session, job: schemas.jobCreate, owner_id: int):
    db_job = models.Job(**job.dict(), owner_id=owner_id)
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    return db_job

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def create_application(db: Session, job_id: int, user_id: int):
    db_application = models.Application(job_id=job_id, applicant_id=user_id)
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

def get_applications(db: Session, job_id: int, user_id: int):
    return db.query(models.Application).filter(models.Application.job_id == job_id, models.Application.applicant_id == user_id).first()   

def update_job(db: Session, job_id: int, job_data: schemas.jobUpdate):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return None

    job.title = job_data.title
    job.description = job_data.description
    job.company = job_data.company
    job.location = job_data.location

    db.commit()
    db.refresh(job)

    return job


def delete_job(db: Session, job_id: int):
    job = db.query(models.Job).filter(models.Job.id == job_id).first()

    if not job:
        return None

    db.delete(job)
    db.commit()

    return job
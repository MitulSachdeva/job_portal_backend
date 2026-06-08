from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from database import Base
from sqlalchemy import Text
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="seeker") #Seeker and Hirer
    is_active = Column(Boolean, default=True)

    jobs = relationship("Job", back_populates="hirer")
    applications = relationship("Application", back_populates="applicant")      
    phone_number = Column(String, nullable=True)

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    company = Column(String)
    location = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))

    hirer = relationship("User", back_populates="jobs")
    applications = relationship("Application", back_populates="job")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    applicant_id = Column(Integer, ForeignKey("users.id"))
    status = Column(String, default="pending")    

    job = relationship("Job", back_populates="applications")
    applicant = relationship("User", back_populates="applications")
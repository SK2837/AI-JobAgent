from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum
from .database import Base

class ApplicationStatus(str, enum.Enum):
    PENDING = "pending"
    SUBMITTED = "submitted"
    FAILED = "failed"
    INTERVIEW = "interview"
    REJECTED = "rejected"

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    company = Column(String, index=True)
    description = Column(Text)
    url = Column(String, unique=True, index=True)
    source = Column(String) # e.g., "linkedin", "indeed"
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    applications = relationship("Application", back_populates="job")

class Resume(Base):
    __tablename__ = "resumes"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text) # Markdown or JSON representation of the resume
    base_resume = Column(Boolean, default=False) # Is this a master resume?
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    applications = relationship("Application", back_populates="resume")

class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    resume_id = Column(Integer, ForeignKey("resumes.id"))
    status = Column(String, default=ApplicationStatus.PENDING)
    submitted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    job = relationship("Job", back_populates="applications")
    resume = relationship("Resume", back_populates="applications")

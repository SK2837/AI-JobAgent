from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from .database import get_db, engine, Base
from .models import Job, Resume, Application, ApplicationStatus
from .services.scraper import ScraperFactory
from .services.resume import ResumeBuilder
from .services.submitter import ApplicationSubmitter
import logging

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Job Agent")
logger = logging.getLogger(__name__)

# Services
resume_builder = ResumeBuilder()
submitter = ApplicationSubmitter()

# Pydantic Models
class JobRequest(BaseModel):
    url: str

class ResumeRequest(BaseModel):
    base_resume: str
    job_description: str

class ApplicationRequest(BaseModel):
    job_id: int
    resume_id: int

@app.get("/")
async def root():
    return {"message": "Welcome to the AI Job Agent API"}

@app.post("/jobs/scrape")
async def scrape_job(request: JobRequest, db: Session = Depends(get_db)):
    try:
        scraper = ScraperFactory.get_scraper(request.url)
        job = await scraper.scrape_job(request.url)
        
        # Save to DB
        db_job = Job(
            title=job.title,
            company=job.company,
            description=job.description,
            url=job.url,
            source=job.source
        )
        db.add(db_job)
        db.commit()
        db.refresh(db_job)
        return db_job
    except Exception as e:
        logger.error(f"Scraping error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/resumes/tailor")
async def tailor_resume(request: ResumeRequest, db: Session = Depends(get_db)):
    try:
        tailored_content = await resume_builder.tailor_resume(request.base_resume, request.job_description)
        
        # Save to DB
        db_resume = Resume(content=tailored_content, base_resume=False)
        db.add(db_resume)
        db.commit()
        db.refresh(db_resume)
        return db_resume
    except Exception as e:
        logger.error(f"Resume tailoring error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/applications/submit")
async def submit_application(request: ApplicationRequest, db: Session = Depends(get_db)):
    job = db.query(Job).filter(Job.id == request.job_id).first()
    resume = db.query(Resume).filter(Resume.id == request.resume_id).first()
    
    if not job or not resume:
        raise HTTPException(status_code=404, detail="Job or Resume not found")
        
    application = Application(job_id=job.id, resume_id=resume.id, status=ApplicationStatus.PENDING)
    db.add(application)
    db.commit()
    db.refresh(application)
    
    # Trigger submission
    # Note: In a real app, this should be a background task (Celery/Arq)
    status = await submitter.submit_application(application)
    
    application.status = status
    db.commit()
    db.refresh(application)
    
    return application


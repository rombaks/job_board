from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from db.repository.jobs import create_new_job, list_jobs, retrieve_job
from db.session import get_db
from schemas.jobs import JobCreate, ShowJob


router = APIRouter()


@router.post("/create-job/", response_model=ShowJob)
def create_job(job: JobCreate, db: Session = Depends(get_db)):
    current_user = 1
    job = create_new_job(job=job, db=db, owner_id=current_user)
    return job


@router.get("/get/{id}", response_model=ShowJob)
def read_job(id: int, db: Session = Depends(get_db)):
    job = retrieve_job(id=id, db=db)
    if not job:
        status_code = status.HTTP_404_NOT_FOUND
        detail = f"Job with this id {id} does not exist"
        raise HTTPException(status_code=status_code, detail=detail)
    return job


@router.get("/all/", response_model=list[ShowJob])
def read_jobs(db: Session = Depends(get_db)):
    jobs = list_jobs(db=db)
    return jobs

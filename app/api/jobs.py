from fastapi import APIRouter, HTTPException

from app.models.memory import RecruitmentRepository
from app.schema.job import JobCreate

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
)

repo = RecruitmentRepository()


@router.post("/")
def create_job(job: JobCreate):

    return repo.add_job(
        title=job.title,
        required_skills=job.required_skills,
        preferred_skills=job.preferred_skills,
        minimum_experience=job.minimum_experience,
        education=job.education,
    )


# @router.get("/")
# def get_jobs():

#     return repo.get_jobs()


@router.get("/{job_id}")
def get_job(job_id: int):

    job = repo.get_jobs(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return job


@router.put("/{job_id}")
def update_job(
    job_id: int,
    job: JobCreate,
):

    updated = repo.update_job(
        job_id,
        job.model_dump(),
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return updated


@router.delete("/{job_id}")
def delete_job(job_id: int):

    deleted = repo.delete_job(job_id)

    if not deleted:
        raise HTTPException(
            status_code=404,
            detail="Job not found",
        )

    return {
        "message": "Job deleted successfully"
    }
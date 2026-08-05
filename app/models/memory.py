from sqlmodel import Session, select

from app.models.db import engine
from app.models.model import (
    Candidate,
    JobRequirement,
    Evaluation
)



class RecruitmentRepository:


    def add_candidate(
        self,
        name:str,
        email:str,
        phone:str,
        resume_path:str
    ):

        with Session(engine) as session:

            candidate = Candidate(
                name=name,
                email=email,
                phone=phone,
                resume_path=resume_path
            )

            session.add(candidate)

            session.commit()

            session.refresh(candidate)

            return candidate



    def get_candidate_by_email(
        self,
        email:str
    ):

        with Session(engine) as session:

            statement = (
                select(Candidate)
                .where(
                    Candidate.email == email
                )
            )

            return session.exec(statement).first()



    def add_job(
        self,
        title: str,
        required_skills: str,
        preferred_skills: str,
        minimum_experience: int,
        education: str,
    ):

        with Session(engine) as session:

            job = JobRequirement(
                title=title,
                required_skills=required_skills,
                preferred_skills=preferred_skills,
                minimum_experience=minimum_experience,
                education=education,
            )

            session.add(job)

            session.commit()

            session.refresh(job)

            return job

    def get_jobs(self, job_id: int):

        with Session(engine) as session:

           statement = (
            select(JobRequirement)
            .where(JobRequirement.id == job_id)
        )

        return session.exec(statement).first()

    def delete_job(self, job_id: int):

        with Session(engine) as session:

            job = session.get(JobRequirement, job_id)

            if not job:
                return None

            session.delete(job)

            session.commit()

            return True

    def update_job(self, job_id: int, data: dict):

        with Session(engine) as session:

            job = session.get(JobRequirement, job_id)

            if not job:
                return None

            for key, value in data.items():
                setattr(job, key, value)

            session.add(job)

            session.commit()

            session.refresh(job)

            return job


    def add_evaluation(
        self,
        candidate_id:int,
        job_id:int,
        score:int,
        recommendation:str,
        strength:str,
        weakness:str
    ):

        with Session(engine) as session:

            evaluation = Evaluation(
                candidate_id=candidate_id,
                job_id=job_id,
                score=score,
                recommendation=recommendation,
                strength=strength,
                weakness=weakness
            )

            session.add(evaluation)

            session.commit()

            session.refresh(evaluation)

            return evaluation
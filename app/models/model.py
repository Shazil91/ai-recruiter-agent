from datetime import UTC, datetime
from typing import Optional

from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB
from sqlmodel import SQLModel, Field

class JobRequirement(SQLModel, table=True):

    __tablename__ = "job_requirements"


    id: Optional[int] = Field(
        default=None,
        primary_key=True
    )


    title: str = Field(
        index=True
    )


    required_skills: list[str] = Field(
        sa_column=Column(JSONB)
    )


    preferred_skills: list[str] = Field(
        sa_column=Column(JSONB)
    )


    minimum_experience: int


    education: list[str] = Field(
        sa_column=Column(JSONB)
    )


    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class Candidate(SQLModel, table=True):
    __tablename__ = "candidates"

    id: Optional[int] = Field(default=None, primary_key=True)

    name: str

    email: str = Field(index=True)

    phone: Optional[str] = None

    resume_path: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )


class Evaluation(SQLModel, table=True):
    __tablename__ = "evaluations"

    id: Optional[int] = Field(default=None, primary_key=True)

    candidate_id: int = Field(
        foreign_key="candidates.id",
        index=True,
    )

    job_id: int = Field(
        foreign_key="job_requirements.id",
        index=True,
    )

    score: int

    recommendation: str

    strengths: str

    weaknesses: str

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC)
    )
    

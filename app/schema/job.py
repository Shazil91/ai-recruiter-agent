from typing import Optional

from pydantic import BaseModel


class JobCreate(BaseModel):

    title: str

    required_skills: str

    preferred_skills: Optional[str] = None

    minimum_experience: int

    education: str


class JobResponse(BaseModel):

    id: int

    title: str

    required_skills: str

    preferred_skills: Optional[str]

    minimum_experience: int

    education: str
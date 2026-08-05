from typing import Optional
from pydantic import BaseModel


class Education(BaseModel):

    degree: Optional[str] = None

    university: Optional[str] = None

    year: Optional[str] = None



class Project(BaseModel):

    name: Optional[str] = None

    description: Optional[str] = None

    technologies: list[str] = []

    github: Optional[str] = None

    live_url: Optional[str] = None



class Candidate(BaseModel):

    name: Optional[str] = None

    email: Optional[str] = None

    phone: Optional[str] = None


    skills: list[str] = []


    experience: Optional[str] = None


    education: list[Education] = []


    certifications: list[str] = []


    projects: list[Project] = []


    linkedin: Optional[str] = None


    github: Optional[str] = None
    
    
class Certification(BaseModel):

    name: str

    organization: Optional[str] = None

    year: Optional[str] = None 
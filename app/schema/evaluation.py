from pydantic import BaseModel
from typing import List

class Evaluation(BaseModel):

    overall_score: int

    recommendation: str

    matched_skills: List[str]

    missing_skills: List[str]

    strengths: List[str]

    weaknesses: List[str]

    interview_questions: List[str]
    
    
import json
from app.core.gemini import ask_gemini
from app.schema.candidate import Candidate
from app.models.model import JobRequirement
from app.schema.evaluation import Evaluation



class GeminiEvaluation:


    def evaluate(
        self,
        candidate: Candidate,
        job: JobRequirement
    ) -> Evaluation:


        prompt = f"""

You are a Senior Technical Recruiter.

Evaluate this candidate for this job.


Candidate Information:

Name:
{candidate.name}

Skills:
{candidate.skills}

Experience:
{candidate.experience}

Education:
{candidate.education}

Certifications:
{candidate.certifications}

Projects:
{candidate.projects}



Job Requirement:

Title:
{job.title}

Required Skills:
{job.required_skills}

Preferred Skills:
{job.preferred_skills}

Experience Required:
{job.minimum_experience}

Education:
{job.education}



Return ONLY valid JSON.

{{
"overall_score":0,

"recommendation":"Interview",

"matched_skills":[],

"missing_skills":[],

"strengths":[],

"weaknesses":[],

"interview_questions":[]
}}

"""


        response = ask_gemini(prompt)


        response = (
            response
            .replace("```json","")
            .replace("```","")
            .strip()
        )


        data = json.loads(response)


        return Evaluation(**data)
    
    
    
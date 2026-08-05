from app.models.memory import RecruitmentRepository
from app.tools.gemini_evaluation import GeminiEvaluation
from app.schema.candidate import Candidate
from app.schema.evaluation import Evaluation

class CandidateEvaluationAgent:

    def __init__(self):

        self.repository = RecruitmentRepository()

        self.gemini = GeminiEvaluation()


    def evaluate(
        self,
        candidate: Candidate,
        job_id: int
    ) -> Evaluation:

        job = self.repository.get_jobs(job_id)

        if not job:

            raise Exception(
                "Job not found"
            )


        result = self.gemini.evaluate(
            candidate,
            job
        )


        return result
    
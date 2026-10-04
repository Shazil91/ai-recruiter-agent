from app.models.memory import RecruitmentRepository
from app.tools.resume_parser import ResumeParserAgent
from app.tools.candidate_evaluate import CandidateEvaluationAgent
from app.tools.calendar import CalendarTool
from app.tools.send_email import GmailTool

class SupervisorAgent:

    def __init__(self):

        self.memory = RecruitmentRepository()

        self.resume_parser = ResumeParserAgent()

        self.candidate_evaluator = CandidateEvaluationAgent()

        self.calendar = CalendarTool()

        self.email = GmailTool()

    def process_resume(
        self,
        file_path: str,
        job_id: int
    ):

        # 1. Parse resume

        candidate_data = self.resume_parser.run(
            file_path
        )

        # 2. Save candidate

        candidate = self.memory.add_candidate(
            name=candidate_data.name,
            email=candidate_data.email,
            phone=candidate_data.phone,
            resume_path=file_path
        )

        # 3. Evaluate candidate

        evaluation = self.candidate_evaluator.evaluate(
            candidate=candidate_data,
            job_id=job_id
        )

        # 4. Save complete evaluation

        self.memory.add_evaluation(
            candidate_id=candidate.id,
            job_id=job_id,
            score=evaluation.score,
            recommendation=evaluation.recommendation,
            matched_skills=evaluation.matched_skills,
            missing_skills=evaluation.missing_skills,
            strengths=evaluation.strengths,
            weaknesses=evaluation.weaknesses,
            interview_questions=evaluation.interview_questions,
        )

        # 5. Decision

        if evaluation.score >= 80:

            # Schedule interview

            calendar_result = self.calendar.run(
                {
                    "title":
                    f"Technical Interview - {candidate.name}",

                    "candidate_email":
                    candidate.email,
                }
            )

            # Send email

            email_result = self.email.run(
                {
                    "to_email": candidate.email,

                    "subject":
                    "Interview Invitation",

                    "body":
                    f"""
      Hello {candidate.name},

      Congratulations!

      You have been shortlisted for a technical interview.

      Your interview has been scheduled on Google Calendar.

      You will receive a calendar invitation with the
      interview details.

      Regards,
      Recruitment Team
      """
                }
            )

            status = "Interview Scheduled"

        elif evaluation.score >= 60:

            email_result = self.email.run(
                {
                    "to_email": candidate.email,

                    "subject":
                    "Application Update",

                    "body":
                    f"""
      Hello {candidate.name},

      Thank you for applying.

      Your application is currently under review.

      We will contact you if you are selected for the next stage.

      Regards,
      Recruitment Team
      """
                }
            )

            calendar_result = None

            status = "On Hold"

        else:

            email_result = self.email.run(
                {
                    "to_email": candidate.email,

                    "subject":
                    "Application Status",

                    "body":
                    f"""
      Hello {candidate.name},

      Thank you for taking the time to apply.

      After reviewing your application, we will not be
      moving forward with your application at this time.

      We appreciate your interest.

      Regards,
      Recruitment Team
      """
                }
            )

            calendar_result = None

            status = "Rejected"

        return {
            "candidate": candidate,
            "evaluation": evaluation,
            "status": status,
            "email": email_result,
            "calendar": calendar_result,
        }
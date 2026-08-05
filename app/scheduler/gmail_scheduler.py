from apscheduler.schedulers.background import BackgroundScheduler

from app.tools.gmail_monitoring import GmailMonitoringTool
from app.agents.supervisor import SupervisorAgent



class GmailScheduler:


    def __init__(self):

        self.gmail = GmailMonitoringTool()

        self.supervisor = SupervisorAgent()

        self.job_id = 1

        self.scheduler = BackgroundScheduler()



    def check_new_resumes(self):

        print(
            "Checking new emails..."
        )


        resume = self.gmail.run()


        if resume:


            print(
                "Resume received:",
                resume["file_path"]
            )


            result = self.supervisor.process_resume(
                file_path=resume["file_path"],
                job_id=self.job_id
            )


            print(
                result
            )


        else:

            print(
                "No new resumes found"
            )



    def start(self):

        self.scheduler.add_job(
            self.check_new_resumes,
            trigger="interval",
            minutes=2
        )


        self.scheduler.start()


        print(
            "Gmail scheduler started..."
        )



    def shutdown(self):

        self.scheduler.shutdown()

        print(
            "Gmail scheduler stopped..."
        )
from app.tools.send_email import GmailTool


gmail = GmailTool()

result = gmail.run({
    "to_email": "syedshazilali28@gmail.com",
    "subject": "AI Recruiter Gmail Test",
    "body": """
Hello,

This is a test email from my AI Recruiter Agent.

Regards,
AI Recruiter
"""
})

print(result)
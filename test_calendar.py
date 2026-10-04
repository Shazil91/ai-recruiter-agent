from app.tools.calendar import CalendarTool


calendar = CalendarTool()

result = calendar.run({
    "title": "AI Recruiter Test Interview",
    "candidate_email": "shazilali312@gmail.com"
})

print(result)
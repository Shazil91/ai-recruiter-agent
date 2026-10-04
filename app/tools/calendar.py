import os

from datetime import datetime, timedelta

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]

TOKEN_FILE = "token_calendar.json"


class CalendarTool:

    def name(self):
        return "calendar"

    def authenticate(self):

        creds = None

        if os.path.exists(TOKEN_FILE):
            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build(
            "calendar",
            "v3",
            credentials=creds
        )

    def run(self, input: dict):

        service = self.authenticate()

        start_time = datetime.utcnow()
        end_time = start_time + timedelta(hours=1)

        event = {
            "summary": input["title"],

            "start": {
                "dateTime": start_time.isoformat() + "Z",
                "timeZone": "UTC",
            },

            "end": {
                "dateTime": end_time.isoformat() + "Z",
                "timeZone": "UTC",
            },

            "attendees": [
                {
                    "email": input["candidate_email"]
                }
            ],
        }

        created_event = service.events().insert(
            calendarId="primary",
            body=event,
            sendUpdates="all"
        ).execute()

        return {
            "status": "scheduled",
            "event_id": created_event["id"],
            "calendar_link": created_event.get("htmlLink")
        }
        
import os
import base64

from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly",
    "https://www.googleapis.com/auth/gmail.send",
]

TOKEN_FILE = "token.json"
CREDENTIALS_FILE = "credentials.json"


class GmailTool:

    def name(self):
        return "gmail"

    def authenticate(self):

        creds = None

        # Load existing token
        if os.path.exists(TOKEN_FILE):

            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )

        # Refresh expired token
        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        # First-time authentication
        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )

            creds = flow.run_local_server(
                port=0
            )

            with open(TOKEN_FILE, "w") as token:
                token.write(creds.to_json())

        return build(
            "gmail",
            "v1",
            credentials=creds
        )

    def run(self, input_data: dict):

        service = self.authenticate()

        message = MIMEText(
            input_data["body"]
        )

        message["to"] = input_data["to_email"]

        message["subject"] = input_data["subject"]

        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode()

        sent = service.users().messages().send(
            userId="me",
            body={
                "raw": raw_message
            }
        ).execute()

        return {
            "status": "sent",
            "message_id": sent["id"]
        }
import os
import base64
from pathlib import Path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build



SCOPES = [
    "https://www.googleapis.com/auth/gmail.readonly"
]


TOKEN_FILE = "token.json"

CREDENTIALS_FILE = "credentials.json"


RESUME_FOLDER = "storage/resumes"


class GmailMonitoringTool:


    def name(self):

        return "gmail_monitor"


    def authenticate(self):

        creds=None


        if os.path.exists(TOKEN_FILE):

            creds = Credentials.from_authorized_user_file(
                TOKEN_FILE,
                SCOPES
            )


        if not creds or not creds.valid:

            flow = InstalledAppFlow.from_client_secrets_file(
                CREDENTIALS_FILE,
                SCOPES
            )


            creds = flow.run_local_server(
                port=0
            )

            with open(
                TOKEN_FILE,
                "w"
            ) as token:

                token.write(
                    creds.to_json()
                )


        return build(
            "gmail",
            "v1",
            credentials=creds
        )



    def run(self):

        service = self.authenticate()


        results = service.users().messages().list(
            userId="me",
            q="is:unread"
        ).execute()

        messages = results.get(
            "messages",
            []
        )


        if not messages:

            return None

        os.makedirs(
            RESUME_FOLDER,
            exist_ok=True
        )


        for msg in messages:

            message_id = msg["id"]

            message = service.users().messages().get(
                userId="me",
                id=message_id
            ).execute()



            parts = message.get(
                "payload",
                {}
            ).get(
                "parts",
                []
            )
  

            for part in parts:


                filename = part.get(
                    "filename"
                )


                if not filename:
                    continue

                extension = Path(filename).suffix.lower()



                if extension not in [
                    ".pdf",
                    ".docx"
                ]:
                    continue

                attachment_id = part["body"]["attachmentId"]

                attachment = service.users().messages().attachments().get(
                    userId="me",
                    messageId=message_id,
                    id=attachment_id
                ).execute()



                file_data = base64.urlsafe_b64decode(
                    attachment["data"]
                )



                file_path = os.path.join(
                    RESUME_FOLDER,
                    filename
                )


                with open(
                    file_path,
                    "wb"
                ) as f:

                    f.write(
                        file_data
                    )

                return {
                    "file_path": file_path,
                    "email_id": message_id
                }
                
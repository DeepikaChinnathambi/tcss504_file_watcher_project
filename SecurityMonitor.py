from email.mime.multipart import MIMEMultipart

from observable import Observable
import base64
import mimetypes
import os.path
from email.message import EmailMessage
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.text import MIMEText

# make sure you pip install the following command
# pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import base64
from email.message import EmailMessage

import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

"""currently mostly copied from https://developers.google.com/gmail/api/guides/sending#python from Tom"""

class SecurityMonitor:
    def __init__(self, db_file=None, message=None, subject=None):

        self.db_file = db_file
        self.message = message if message is not None else "This is an automated alert message from Guard Dog. Please see attached .zip file for log database."
        self.subject = subject if subject is not None else "File Watcher Log"


    def send_email(self):
        """Create and insert a draft email with attachment.
         Print the returned draft's message and id.
        Returns: Draft object, including draft id and message meta data.

        Load pre-authorized user credentials from the environment.
        TODO(developer) - See https://developers.google.com/identity
        for guides on implementing OAuth2 for the application.
        """


        try:
            # creds, _ = google.auth.default()

            # If modifying these scopes, delete the file token.json.
            SCOPES = ["https://mail.google.com/"]

            creds = None
            # The file token.json stores the user's access and refresh tokens, and is
            # created automatically when the authorization flow completes for the first
            # time.
            if os.path.exists("token.json"):
                creds = Credentials.from_authorized_user_file("token.json", SCOPES)
            # If there are no (valid) credentials available, let the user log in.
            if not creds or not creds.valid:
                if creds and creds.expired and creds.refresh_token:
                    creds.refresh(Request())
                else:
                    flow = InstalledAppFlow.from_client_secrets_file(
                        "token.json", SCOPES
                    )
                    creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open("token.json", "w") as token:
              token.write(creds.to_json())

            # create gmail api client
            service = build("gmail", "v1", credentials=creds)
            message = EmailMessage()

            # Log in info
            # receiver PW - filereceiver1!
            # sender PW - filesender1234!
            message["To"] = "filereceiver99@gmail.com"
            message["From"] = "filewatchersender@gmail.com"
            message["Subject"] = self.subject

            # text
            message.set_content(self.message)

            # guessing the MIME type
            type_subtype, _ = mimetypes.guess_type(self.db_file)
            maintype, subtype = type_subtype.split("/")

            with open(self.db_file, "rb") as fp:
                attachment_data = fp.read()
            message.add_attachment(attachment_data, maintype, subtype)

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

            create_message = {"raw": encoded_message}
            # pylint: disable=E1101
            send_message = (
                service.users()
                .messages()
                .send(userId="me", body=create_message)
                .execute()
            )
            print(f'Message id: {send_message["id"]}\nMessage message: {send_message}')

        except HttpError as error:
            print(f"An error occurred: {error}")
            send_message = None

        return send_message


    def build_file_part(self, file):
        """Creates a MIME part for a file.
        Args:
          file: The path to the file to be attached.
        Returns:
          A MIME part that can be attached to a message.
        """
        content_type, encoding = mimetypes.guess_type(file)

        if content_type is None or encoding is not None:
            content_type = "application/octet-stream"

        main_type, sub_type = content_type.split("/", 1)

        if main_type == "text":
            with open(file, "rb"):
                msg = MIMEText("r", _subtype=sub_type)

        elif main_type == "image":
            with open(file, "rb"):
                msg = MIMEImage("r", _subtype=sub_type)

        elif main_type == "audio":
            with open(file, "rb"):
                msg = MIMEAudio("r", _subtype=sub_type)

        else:
            with open(file, "rb"):
                msg = MIMEBase(main_type, sub_type)
                msg.set_payload(file.read())

        filename = os.path.basename(file)
        msg.add_header("Content-Disposition", "attachment", filename=filename)
        return msg









import base64
from email.message import EmailMessage
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from config import SCOPES


def get_gmail_service():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials.json", SCOPES
    )
    creds = flow.run_local_server(port=0)
    return build("gmail", "v1", credentials=creds)


def read_sent_emails(service, max_results=20):
    results = service.users().messages().list(
        userId="me",
        labelIds=["SENT"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        parts = msg_data.get("payload", {}).get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    text = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )
                    emails.append(text.strip())
    return emails


def read_inbox_emails(service, max_results=3):
    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=max_results
    ).execute()

    messages = results.get("messages", [])
    emails = []

    for msg in messages:
        msg_data = service.users().messages().get(
            userId="me", id=msg["id"], format="full"
        ).execute()

        parts = msg_data.get("payload", {}).get("parts", [])
        for part in parts:
            if part.get("mimeType") == "text/plain":
                data = part.get("body", {}).get("data")
                if data:
                    text = base64.urlsafe_b64decode(data).decode(
                        "utf-8", errors="ignore"
                    )
                    emails.append(text.strip())
    return emails


def save_to_drafts(service, to_email, subject, body):
    msg = EmailMessage()
    msg.set_content(body)
    msg["To"] = to_email
    msg["Subject"] = subject

    encoded = base64.urlsafe_b64encode(msg.as_bytes()).decode()

    service.users().drafts().create(
        userId="me",
        body={"message": {"raw": encoded}}
    ).execute()

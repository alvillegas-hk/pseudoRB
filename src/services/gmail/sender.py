import logging
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials

log = logging.getLogger("gmail.sender")


def send_raw_message(
    creds: Credentials,
    raw_message: str,
) -> None:
    service = build("gmail", "v1", credentials=creds, cache_discovery=False)

    service.users().messages().send(
        userId="me",
        body={"raw": raw_message}
    ).execute()
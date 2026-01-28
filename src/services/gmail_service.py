import base64
import logging
from email.message import EmailMessage
from pathlib import Path
from typing import Optional

from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

log = logging.getLogger("gmail_service")

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


class GmailClient:
    def __init__(
        self,
        credentials_json: Path,
        token_json: Path,
        sender: str,
    ) -> None:
        self.credentials_json = credentials_json
        self.token_json = token_json
        self.sender = sender
        self.creds: Optional[Credentials] = None
        self.service = None

    def authenticate(self) -> None:
        if self.token_json.exists():
            self.creds = Credentials.from_authorized_user_file(
                str(self.token_json), SCOPES
            )

        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                log.info("Refrescando token Gmail")
                self.creds.refresh(Request())
            else:
                log.info("Iniciando OAuth Gmail")
                flow = InstalledAppFlow.from_client_secrets_file(
                    str(self.credentials_json), SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            self.token_json.parent.mkdir(parents=True, exist_ok=True)
            self.token_json.write_text(self.creds.to_json(), encoding="utf-8")

        self.service = build("gmail", "v1", credentials=self.creds)
        log.info("Gmail autenticado correctamente")


    def send_text(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> None:
        self._send_message(to, subject, body, is_html=False)

    def send_html(
        self,
        to: str,
        subject: str,
        html: str,
    ) -> None:
        self._send_message(to, subject, html, is_html=True)

    def _send_message(
        self,
        to: str,
        subject: str,
        content: str,
        is_html: bool,
    ) -> None:
        if not self.service:
            raise RuntimeError("GmailClient no autenticado")

        if not to:
            raise ValueError("Destinatario vacío")

        msg = EmailMessage()
        msg["From"] = self.sender
        msg["To"] = to
        msg["Subject"] = subject

        if is_html:
            msg.add_alternative(content, subtype="html")
        else:
            msg.set_content(content)

        raw = base64.urlsafe_b64encode(msg.as_bytes()).decode("utf-8")

        self.service.users().messages().send(
            userId="me",
            body={"raw": raw}
        ).execute()

        log.info("Mail enviado → %s | %s", to, subject)

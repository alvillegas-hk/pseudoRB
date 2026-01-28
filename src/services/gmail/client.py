import logging
from pathlib import Path

from .auth import get_credentials
from .message import build_message
from .sender import send_raw_message

log = logging.getLogger("gmail.client")


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
        self.creds = None

    def authenticate(self) -> None:
        self.creds = get_credentials(
            self.credentials_json,
            self.token_json
        )
        log.info("Gmail autenticado correctamente")

    def send_text(
        self,
        to: str,
        subject: str,
        body: str,
    ) -> None:
        self._send(to, subject, body, is_html=False)

    def send_html(
        self,
        to: str,
        subject: str,
        html: str,
    ) -> None:
        self._send(to, subject, html, is_html=True)

    def _send(
        self,
        to: str,
        subject: str,
        content: str,
        is_html: bool,
    ) -> None:
        if not self.creds:
            raise RuntimeError("GmailClient no autenticado")

        if not to:
            raise ValueError("Destinatario vacío")

        raw = build_message(
            sender=self.sender,
            to=to,
            subject=subject,
            content=content,
            is_html=is_html,
        )

        send_raw_message(self.creds, raw)
        log.info("Mail enviado → %s | %s", to, subject)

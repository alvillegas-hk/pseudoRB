import logging
import os
from pathlib import Path
from typing import Optional

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

log = logging.getLogger("gmail.auth")


def get_gmail_scopes() -> list[str]:
    raw = os.getenv("GMAIL_SCOPES", "")
    if not raw:
        raise RuntimeError("GMAIL_SCOPES no definido en el environment")
    return [s.strip() for s in raw.split(",") if s.strip()]


def get_credentials(
    credentials_json: Path,
    token_json: Path,
) -> Credentials:
    scopes = get_gmail_scopes()
    creds: Optional[Credentials] = None

    if token_json.exists():
        creds = Credentials.from_authorized_user_file(
            str(token_json),
            scopes
        )

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            log.info("Refrescando token Gmail")
            creds.refresh(Request())
        else:
            log.info("Iniciando OAuth Gmail")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_json),
                scopes
            )
            creds = flow.run_local_server(port=0)

        token_json.parent.mkdir(parents=True, exist_ok=True)
        token_json.write_text(creds.to_json(), encoding="utf-8")

    return creds

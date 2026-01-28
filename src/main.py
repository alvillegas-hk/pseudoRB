import logging

from config.settings import settings
from config.logging_config import setup_logging
from core.excel_loader import load_observaciones_excel
from core.processing import split_por_estado
from core.validators import validate_excel, validate_url, validate_gmail_files
from services.gmail.client import GmailClient
from services.playwright.runner import process_rows
from core.notifications.auditoria_mailer import notify_atrasados

log = logging.getLogger("main")

def run():
    setup_logging(settings.log_level, settings.log_file)

    validate_excel(settings.excel_path)
    validate_url(settings.form_url)
    validate_gmail_files(
        settings.gmail_credentials_json,
        settings.gmail_token_json
    )

    df = load_observaciones_excel(settings.excel_path, settings.excel_sheet)
    atrasados, regularizados = split_por_estado(df)

    log.info("Atrasados=%s Regularizados=%s", len(atrasados), len(regularizados))

    if atrasados:
        gmail = GmailClient(
            credentials_json=settings.gmail_credentials_json,
            token_json=settings.gmail_token_json,
            sender=settings.gmail_from,
        )
        gmail.authenticate()
        notify_atrasados(gmail, atrasados)

    process_rows(
        settings.form_url,
        settings.playwright_headless,
        settings.playwright_slow_mo_ms,
        regularizados
    )

if __name__ == "__main__":
    run()

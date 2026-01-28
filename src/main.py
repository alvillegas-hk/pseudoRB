import logging

from config.settings import settings
from config.logging_config import setup_logging
from core.excel_loader import load_observaciones_excel
from core.processing import split_por_estado
from core.validators import validate_excel, validate_url, validate_gmail_files
from services.gmail_service import GmailClient
from services.playwright.runner import process_rows
from services.playwright.runner import process_rows

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

    # ==========================
    # GMAIL (una sola sesión)
    # ==========================

    gmail = GmailClient(
        credentials_json=settings.gmail_credentials_json,
        token_json=settings.gmail_token_json,
        sender=settings.gmail_from,
    )
    gmail.authenticate()

    for row in atrasados:
        to = row.get("Correo responsable", "")
        if not to:
            continue

        subject = f"[Auditoría] Observación ATRASADA - {row.get('Auditoria/Proceso','')}"
        body = (
            f"Hola {row.get('Responsable','')},\n\n"
            f"Tenés una observación ATRASADA:\n"
            f"- Proceso: {row.get('Auditoria/Proceso','')}\n"
            f"- Observación: {row.get('Observación','')}\n"
            f"- Plan: {row.get('Plan de Acción','')}\n"
            f"- Fecha compromiso: {row.get('Fecha Compromiso','')}\n"
            f"- Estado: {row.get('Estado','')}\n"
        )

        gmail.send_text(to, subject, body)

    # ==========================
    # PLAYWRIGHT
    # ==========================

    process_rows(
        settings.form_url,
        settings.playwright_headless,
        settings.playwright_slow_mo_ms,
        regularizados
    )

if __name__ == "__main__":
    run()

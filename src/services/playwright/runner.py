import logging
from playwright.sync_api import sync_playwright, TimeoutError

from .mapping import FIELD_INTENT
from .discovery import discover_form_fields
from .resolvers import resolve_field
from .fillers import fill_field
from .submit import submit_form

log = logging.getLogger("playwright.runner")


FORM_READY_SELECTOR = "#process"


def process_rows(
    form_url: str,
    headless: bool,
    slow_mo_ms: int,
    rows: list[dict]
) -> None:

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=headless,
            slow_mo=slow_mo_ms
        )
        context = browser.new_context()
        page = context.new_page()

        page.goto(form_url, wait_until="domcontentloaded")
        page.wait_for_selector(FORM_READY_SELECTOR, timeout=10_000)

        for idx, row in enumerate(rows, start=1):
            log.info("Procesando fila %s", idx)

            try:
                # 🔁 Redescubrir campos (robusto)
                fields = discover_form_fields(page)

                for excel_col, logical_name in FIELD_INTENT.items():
                    field = resolve_field(fields, logical_name)
                    if not field:
                        log.warning("Campo no encontrado: %s", logical_name)
                        continue

                    value = row.get(excel_col)
                    if value in (None, "", "NaT"):
                        continue

                    fill_field(page, field, value)

                submit_form(page)

                page.wait_for_selector(FORM_READY_SELECTOR, timeout=10_000)

            except TimeoutError as e:
                log.error(
                    "Timeout en fila %s | Proceso=%s",
                    idx,
                    row.get("Auditoria/Proceso"),
                    exc_info=e
                )
                continue

            except Exception as e:
                log.error(
                    "Error inesperado en fila %s | Proceso=%s",
                    idx,
                    row.get("Auditoria/Proceso"),
                    exc_info=e
                )
                continue

        browser.close()

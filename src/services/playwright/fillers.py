import logging
from datetime import datetime, timedelta
from typing import Union
from playwright.sync_api import Page

from .models import FormField
from .resolvers import resolve_select_value

log = logging.getLogger("playwright.fillers")

def normalize_date(value: Union[str, int, float, datetime]) -> str:
    if isinstance(value, datetime):
        return value.strftime("%Y-%m-%d")

    if isinstance(value, (int, float)):
        excel_epoch = datetime(1899, 12, 30)
        return (excel_epoch + timedelta(days=int(value))).strftime("%Y-%m-%d")

    value = str(value).strip()
    for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).strftime("%Y-%m-%d")
        except ValueError:
            pass

    raise ValueError(f"Formato de fecha no soportado: {value}")


def build_selector(field: FormField) -> str:
    if field.id:
        return f"#{field.id}"
    if field.name:
        return f"[name='{field.name}']"
    raise ValueError("Campo sin id ni name")


def fill_with_js(page: Page, selector: str, value: str) -> None:
    page.evaluate(
        """
        ({ selector, value }) => {
            const el = document.querySelector(selector);
            if (!el) throw new Error("Elemento no encontrado: " + selector);
            el.value = value;
            el.dispatchEvent(new Event("input", { bubbles: true }));
            el.dispatchEvent(new Event("change", { bubbles: true }));
        }
        """,
        {"selector": selector, "value": value}
    )


def fill_field(page: Page, field: FormField, value) -> None:
    selector = build_selector(field)

    if field.tag == "input" and field.type == "date":
        page.fill(selector, normalize_date(value))
        return

    if field.tag == "select":
        page.select_option(selector, resolve_select_value(field, value))
        return

    fill_with_js(page, selector, str(value))

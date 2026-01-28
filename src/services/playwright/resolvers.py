from typing import Optional
from .models import FormField

def resolve_field(fields: list[FormField], logical_name: str) -> Optional[FormField]:
    for f in fields:
        if f.id == logical_name or f.name == logical_name:
            return f
    return None


def resolve_select_value(field: FormField, excel_value: str) -> str:
    if not field.options:
        raise ValueError("Campo select sin opciones")

    for opt in field.options:
        if opt.label.strip().lower() == str(excel_value).strip().lower():
            return opt.value

    raise ValueError(f"No se pudo mapear '{excel_value}' en select {field.id}")

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv, find_dotenv

# =========================
# Project root
# settings.py → src/config → src → project root
# =========================
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# =========================
# Load environment
# =========================
# Busca el .env aunque el working directory no sea el root del proyecto
load_dotenv(find_dotenv(usecwd=True))

# (Alternativa simple si preferís ruta fija)
# load_dotenv(PROJECT_ROOT / ".env")

# =========================
# Helpers
# =========================
def _required_env(var_name: str) -> str:
    value = os.getenv(var_name)
    if not value:
        raise RuntimeError(
            f"Variable de entorno requerida no definida: {var_name}"
        )
    return value

def _required_path(var_name: str) -> Path:
    value = _required_env(var_name)
    p = Path(value)
    return p if p.is_absolute() else (PROJECT_ROOT / p).resolve()

def _bool(value: str) -> bool:
    return value.strip().lower() in ("1", "true", "yes", "y", "on")

# =========================
# Settings
# =========================
@dataclass(frozen=True)
class Settings:
    # Excel
    excel_path: Path = _required_path("EXCEL_PATH")
    excel_sheet: str = _required_env("EXCEL_SHEET")

    # Logs
    log_level: str = _required_env("LOG_LEVEL")
    log_file: Path = _required_path("LOG_FILE")

    # Gmail
    gmail_from: str = _required_env("GMAIL_FROM")
    gmail_credentials_json: Path = _required_path("GMAIL_CREDENTIALS_JSON")
    gmail_token_json: Path = _required_path("GMAIL_TOKEN_JSON")

    # Playwright / Form
    form_url: str = _required_env("FORM_URL")
    playwright_headless: bool = _bool(_required_env("PLAYWRIGHT_HEADLESS"))
    playwright_slow_mo_ms: int = int(_required_env("PLAYWRIGHT_SLOW_MO_MS"))

settings = Settings()
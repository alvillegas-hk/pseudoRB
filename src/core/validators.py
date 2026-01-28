from pathlib import Path
from urllib.parse import urlparse

def validate_excel(path: Path) -> None:
    if not path.exists():
        raise FileNotFoundError(f"Excel no encontrado: {path}")

def validate_url(url: str) -> None:
    p = urlparse(url)
    if not (p.scheme and p.netloc):
        raise ValueError(f"URL inválida: {url}")

def validate_gmail_files(credentials: Path, token: Path) -> None:
    if not credentials.exists():
        raise FileNotFoundError(f"Falta credentials.json: {credentials}")
    # token.json puede no existir la primera vez (se genera luego del OAuth)

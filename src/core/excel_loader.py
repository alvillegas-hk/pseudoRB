import pandas as pd
import logging
from pathlib import Path

log = logging.getLogger("excel_loader")

def _normalize_col(col: str) -> str:
    col = str(col).replace("\n", " ").strip()
    col = " ".join(col.split())
    return col

def load_observaciones_excel(path: Path, sheet: str) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(f"No existe el Excel: {path}")

    df = pd.read_excel(path, sheet_name=sheet, engine="openpyxl")
    df.columns = [_normalize_col(c) for c in df.columns]

    # Normalización defensiva de nombres esperados
    rename_map = {
        "Auditoría/Proceso": "Auditoria/Proceso",
        "Severidad Observación": "Severidad Observación",
        "Fecha Compromiso": "Fecha Compromiso",
        "Area Responsable": "Area Responsable",
        "Correo responsable": "Correo responsable",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    log.info("Excel cargado: filas=%s cols=%s", len(df), list(df.columns))
    return df

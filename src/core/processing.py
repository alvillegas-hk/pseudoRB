import pandas as pd

def split_por_estado(df: pd.DataFrame) -> tuple[list[dict], list[dict]]:
    # Limpieza mínima
    df = df.copy()
    df["Estado"] = df["Estado"].astype(str).str.strip()

    atrasados = df[df["Estado"].str.lower() == "atrasado"].to_dict(orient="records")
    regularizados = df[df["Estado"].str.lower() == "regularizado"].to_dict(orient="records")

    return atrasados, regularizados

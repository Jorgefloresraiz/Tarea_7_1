"""Perfil reproducible del CSV; no entrena ni modifica datos."""
import hashlib
from pathlib import Path
import pandas as pd


def resumir(ruta='datos/credit_g.csv'):
    ruta = Path(ruta)
    df = pd.read_csv(ruta)
    if 'clase' not in df or not set(df['clase'].dropna()).issubset({'good', 'bad'}):
        raise ValueError('Se requiere clase con etiquetas good/bad.')
    return {
        'filas': len(df), 'columnas': len(df.columns),
        'nulos': int(df.isna().sum().sum()),
        'duplicados': int(df.duplicated().sum()),
        'clases': {str(k): int(v) for k, v in df['clase'].value_counts().sort_index().items()},
        'sha256': hashlib.sha256(ruta.read_bytes()).hexdigest(),
    }

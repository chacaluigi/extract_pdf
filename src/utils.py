import os
from pathlib import Path
from datetime import datetime
import re
from PyPDF2 import PdfReader

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def parse_date_from_filename(filename: str):
    """Intenta extraer fecha YYYYMMDD o YYYY-MM-DD del nombre de archivo."""
    m = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    return None

def normalize_ci(ci_raw: str):
    # elimina todo lo que no sea dígito
    return re.sub(r'\D', '', str(ci_raw)).strip()

def normalize_name(name: str):
    # minúsculas, quitar múltiples espacios, tildes (opcional)
    name = str(name).strip()
    name = re.sub(r'\s+', ' ', name)
    return name.upper()

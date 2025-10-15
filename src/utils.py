import os
from pathlib import Path
from datetime import datetime
import re
from PyPDF2 import PdfReader

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def get_pdf_date(pdf_path: str):
    """Intenta obtener la fecha de creación del PDF desde metadata.
    Si no está, devuelve None (se puede luego usar la fecha en el filename)."""
    try:
        reader = PdfReader(pdf_path)
        info = reader.metadata
        # PyPDF2: info.get('/CreationDate') o info.get('CreationDate')
        raw = info.get('/CreationDate') or info.get('CreationDate') or info.get('/ModDate') or info.get('ModDate')
        if not raw:
            return None
        # Ejemplo formato: D:20250919...
        m = re.search(r'(\d{4})(\d{2})(\d{2})', str(raw))
        if m:
            y, mo, d = m.group(1), m.group(2), m.group(3)
            return datetime(int(y), int(mo), int(d)).date()
    except Exception as e:
        return None

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

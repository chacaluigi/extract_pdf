# src/clean_data.py
import pandas as pd
from pathlib import Path
from src.utils import ensure_dir, normalize_ci, normalize_name, parse_date_from_filename

CLEAN_DIR = Path(__file__).resolve().parents[1] / "data" / "cleaned"

def clean_csv(input_csv: str, output_csv: str = None, source_pdf=None, pdf_date=None):
    ensure_dir(CLEAN_DIR)
    df = pd.read_csv(input_csv, dtype=str, keep_default_na=False)
    # Normalizar columnas: tratar de asignar columnas comunes
    # Ejemplo asumiendo columnas como ["NRO","APELLIDOS","NOMBRES","TIPO DOCUMENTO","NRO. DOCUMENTO", ...]
    # Normalizar nombres de columnas a minúsculas sin espacios
    colmap = {c: c.strip().lower().replace(' ', '_') for c in df.columns}
    df.rename(columns=colmap, inplace=True)

    # Intentos de identificar columnas relevantes:
    possible_ci_cols = [c for c in df.columns if 'doc' in c or 'documento' in c or 'nro' in c or 'dni' in c]
    possible_name_cols = [c for c in df.columns if 'nombre' in c or 'apellidos' in c or 'apell' in c]

    # Construir dataframe canónico
    canonical = pd.DataFrame()
    # Column: ci
    if possible_ci_cols:
        canonical['ci'] = df[possible_ci_cols[0]].apply(normalize_ci)
    else:
        canonical['ci'] = ''

    # Nombres completos
    # intenta combinar apellido + nombre si existen
    apellido_cols = [c for c in df.columns if 'apell' in c]
    nombre_cols = [c for c in df.columns if 'nombre' in c]
    if apellido_cols and nombre_cols:
        canonical['apellidos'] = df[apellido_cols[0]].apply(normalize_name)
        canonical['nombres'] = df[nombre_cols[0]].apply(normalize_name)
    else:
        # fallback: primer posible name column
        if possible_name_cols:
            parts = df[possible_name_cols[0]].str.split(n=1, expand=True)
            canonical['apellidos'] = parts[0].apply(normalize_name)
            canonical['nombres'] = parts[1].fillna('').apply(normalize_name)
        else:
            canonical['apellidos'] = ''
            canonical['nombres'] = ''

    # Otras columnas heurísticas
    for heur in ['municipio', 'recinto', 'mesa', 'tipo']:
        candidates = [c for c in df.columns if heur in c]
        canonical[heur] = df[candidates[0]] if candidates else ''

    canonical['source_csv'] = input_csv
    canonical['source_pdf'] = source_pdf or ''
    canonical['pdf_date'] = pd.to_datetime(pdf_date) if pdf_date is not None else parse_date_from_filename(Path(input_csv).stem)
    # guardar
    if output_csv is None:
        output_csv = CLEAN_DIR / f"{Path(input_csv).stem}_clean.csv"
    canonical.to_csv(output_csv, index=False)
    print(f"Limpieza completada -> {output_csv}")
    return str(output_csv)


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Uso: python clean_data.py <input_csv> [source_pdf] [pdf_date]")
        sys.exit(1)
    input_csv = sys.argv[1]
    source_pdf = sys.argv[2] if len(sys.argv) > 2 else None
    print(source_pdf)
    pdf_date = sys.argv[3] if len(sys.argv) > 3 else None
    clean_csv(input_csv, source_pdf=source_pdf, pdf_date=pdf_date)

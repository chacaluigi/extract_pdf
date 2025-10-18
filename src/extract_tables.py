import os
import sys
from pathlib import Path
import camelot
from src.utils import ensure_dir, parse_date_from_filename

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def extract_pdf_tables(pdf_path: str, output_dir: str = None, pages="all", flavor="stream"):
    pdf_path = Path(pdf_path)
    if output_dir is None:
        output_dir = DATA_DIR / "extracted"
    else:
        output_dir = Path(output_dir)
    
    ensure_dir(output_dir)

    print(f"Extrayendo tablas de: {pdf_path} - flavor={flavor} - pages={pages}")
    tables = camelot.read_pdf(str(pdf_path), pages=pages, flavor=flavor, split_text=True,flag_size=True)
    print(f"Tablas encontradas: {len(tables)}")

    csv_paths = []
    for i, table in enumerate(tables, start=1):
        out_csv = output_dir / f"{pdf_path.stem}_table{i}.csv"
        table.df.to_csv(out_csv, index=False)
        csv_paths.append(str(out_csv))
        print(f"guardado {out_csv} (shape={table.df.shape})")

    pdf_date = parse_date_from_filename(str(pdf_path))
    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_tables.py <pdf_path> [pages] [flavor]")
        sys.exit(1)
    pdf = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else "all"
    flavor = sys.argv[3] if len(sys.argv) > 3 else "stream"
    res = extract_pdf_tables(pdf, pages=pages, flavor=flavor)
    print(res)

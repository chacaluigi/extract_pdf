import pandas as pd
import pdfplumber
import sys
from pathlib import Path
import camelot
import math
from src.utils import ensure_dir, parse_date_from_filename

DATA_DIR = Path(__file__).resolve().parents[1] / "data"

def join_tables_csv(tables, pdf_path, output_dir):
    csv_paths = []

    if len(tables) > 0:
        all_dataframes = []

        for i, table in enumerate(tables, start=1):
            if i == 1:
                all_dataframes.append(table.df)
            else:
                all_dataframes.append(table.df.iloc[1:])
        
        combined_df = pd.concat(all_dataframes, ignore_index=True)
        combined_csv = output_dir / f"{pages}___{pdf_path.stem}.csv"
        combined_df.to_csv(combined_csv, index=False, header=False)
        csv_paths.append(str(combined_csv))
        print(f"guardado en: {combined_csv}  Dimensiones: {combined_df.shape[0]} filas × {combined_df.shape[1]} columnas")
    return csv_paths

def extract_dimensions_page(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[page_number+1]
    return page.width, page.height

def repair_broken_rows_simple(table_list):
    for table in table_list:
        df = table.df.fillna('')  # reemplaza NaN con strings vacíos
        repaired_rows = []
        
        for _, row in df.iterrows():
            # se convierte a strings y se limpia
            row = [str(cell).strip() for cell in row]
            
            #si la primera columna vacía y hay filas anteriores
            if row[0] == '' and repaired_rows:
                # se une con ultima fila
                last_row = repaired_rows[-1]
                for i in range(len(row)):
                    if row[i] != '':
                        last_row[i] = (last_row[i] + ' ' + row[i]).strip()
            else:
                repaired_rows.append(row)
        
        table.df = pd.DataFrame(repaired_rows)
    
    return table_list

def extract_pdf_tables_areas(pdf_path: str, output_dir: str = None, pages="all", flavor="stream"):
    pdf_path = Path(pdf_path)
    if output_dir is None:
        output_dir = DATA_DIR / "extracted"
    else:
        output_dir = Path(output_dir)
    
    ensure_dir(output_dir)

    print(f"Extrayendo tablas de: {pdf_path} --- flavor = {flavor} --- pages = {pages}")

    page_width, page_height = extract_dimensions_page(pdf_path, 6)

    table_areas_list = [
        [f'0,0,{1/3*float(page_width)},{page_height}'],
        [f'{1/3*float(page_width)},0,{2/3*float(page_width)},{page_height}'],
        [f'{2/3*float(page_width)},0,{page_width},{page_height}']
    ]

    tables=[]
    
    for _, table_areas in enumerate(table_areas_list):
        table_list = camelot.read_pdf(str(pdf_path), pages=pages, flavor=flavor, split_text=True, flag_size=True, table_areas=table_areas)
        repaired_tables = repair_broken_rows_simple(table_list)
        tables.extend(repaired_tables)

    print(f"Cantidad de tablas encontradas: {len(tables)}")
    
    cols = 3
    reason = math.ceil(len(tables)/cols)

    tables_ordered = [tables[j] for i in range(reason) for j in range(i, len(tables), reason)]

    tables = tables_ordered
    print('Primera tabla')
    print(tables[0].df)
    print('segunda tabla')
    print(tables[1].df)
    print('tercera tabla')
    print(tables[2].df)
    print('cuarta tabla')
    print(tables[3].df)
    
    csv_paths = join_tables_csv(tables, pdf_path, output_dir) 

    pdf_date = parse_date_from_filename(str(pdf_path))
    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}


def extract_pdf_tables(pdf_path: str, output_dir: str = None, pages="all", flavor="stream"):
    pdf_path = Path(pdf_path)
    
    if output_dir is None:
        output_dir = DATA_DIR / "extracted"
    else:
        output_dir = Path(output_dir)
    
    ensure_dir(output_dir)

    print(f"Extrayendo tablas de: {pdf_path} --- flavor = {flavor} --- pages = {pages}")

    tables = camelot.read_pdf(str(pdf_path), pages=pages, flavor=flavor, split_text=True, flag_size=True)
    print(f"Tablas encontradas: {len(tables)}")

    csv_paths = []

    if len(tables) > 0:
        all_dataframes = []

        for i, table in enumerate(tables, start=1):
            if i == 1:
                all_dataframes.append(table.df)
            else:
                all_dataframes.append(table.df.iloc[1:])
        
        combined_df = pd.concat(all_dataframes, ignore_index=True)

        combined_csv = output_dir / f"{pdf_path.stem}_combined.csv"
        combined_df.to_csv(combined_csv, index=False, header=False)
        csv_paths.append(str(combined_csv))
        print(f"guardado en: {combined_csv}  Dimensiones: {combined_df.shape[0]} filas × {combined_df.shape[1]} columnas")

    pdf_date = parse_date_from_filename(str(pdf_path))
    return {"pdf": str(pdf_path), "pdf_date": pdf_date, "csvs": csv_paths}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python extract_tables.py <pdf_path> [pages] [flavor]")
        sys.exit(1)
    pdf = sys.argv[1]
    pages = sys.argv[2] if len(sys.argv) > 2 else "all"
    flavor = sys.argv[3] if len(sys.argv) > 3 else "stream"
    #res = extract_pdf_tables(pdf, pages=pages, flavor=flavor)
    res = extract_pdf_tables_areas(pdf, pages=pages, flavor=flavor)

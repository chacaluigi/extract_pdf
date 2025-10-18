import pandas as pd
from pathlib import Path
from src.utils import ensure_dir, normalize_ci, normalize_name, parse_date_from_filename
import sys

CLEAN_DIR = Path(__file__).resolve().parents[1] / "data" / "cleaned"
DATA_BOL_DIR = Path(__file__).resolve().parents[1] / "data" / "dictionary"

from data.dictionary.data_bolivia import BoliviaData
nombres_bolivia = BoliviaData.NOMBRES

def clear_ci_document(df):
    processed_df=df.copy()
    processed_df["DOCUMENTO"]=processed_df['DOCUMENTO'].str.replace(r'^I\-\s*','', regex=True)
    return processed_df

def separate_last_and_first_names(text):

    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts=str(text).strip().split()

    if len(parts) < 2:
        print(f'ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menos de 2 palabras.')
        return pd.Series([text, '', ''])
    
    conectors={'de', 'del', 'la', 'tezanos', 'le'}

    processed_parts = []
    i=0
    while i<len(parts):
        current_part=parts[i]

        if current_part.lower() in conectors and parts[i+1].lower() in conectors and i+2 < len(parts):
            combined = f"{current_part} {parts[i+1]} {parts[i+2]}"
            processed_parts.append(combined)
            i+=3
        elif current_part.lower() in conectors and i+1<len(parts):
            combined = f"{current_part} {parts[i+1]}"
            processed_parts.append(combined)
            i+=2
        else:
            processed_parts.append(current_part)
            i+=1
    
    parts=processed_parts

    if len(parts) == 2:
        pat_surname=''
        mat_surname=parts[0]
        names=parts[1]

    elif len(parts) == 3:
        if parts[1] in nombres_bolivia:
            pat_surname=""
            mat_surname=parts[0]
            names=f'{parts[1]} {parts[2]}'
        else:
            pat_surname=parts[0]
            mat_surname=parts[1]
            names=parts[2]
    else:
        pat_surname=parts[0]
        mat_surname=parts[1]
        names = ' '.join(parts[2:])
    
    return pd.Series([pat_surname, mat_surname, names])

def clean_csv(input_csv: str, output_csv: str = None, source_pdf=None, pdf_date=None):
    
    ensure_dir(CLEAN_DIR)
    df = pd.read_csv(input_csv, dtype=str, keep_default_na=False)
    df = clear_ci_document(df)

    if 'APELLIDOS Y NOMBRES' in df.columns:
        nombre_split = df['APELLIDOS Y NOMBRES'].apply(separate_last_and_first_names)
        df[['APELLIDO_PATERNO', 'APELLIDO_MATERNO', 'NOMBRES']] = nombre_split

        df = df.drop('APELLIDOS Y NOMBRES', axis=1)

    if source_pdf:
        df['FUENTE_PDF'] = source_pdf
    
    if pdf_date:
        df['FECHA_PDF'] = pdf_date
    elif source_pdf:
        extracted_date = parse_date_from_filename(source_pdf)
        if extracted_date:
            df['FECHA_PDF'] = extracted_date

    if output_csv is None:
        input_path = Path(input_csv)
        output_csv = CLEAN_DIR / f"{input_path.name}_clean.csv"

    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"Archivo limpio guardado en: {output_csv}")

    return df

if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("Solo un argumento. Colocar los argumentos correctos, ver .README")
    else:
        if len(sys.argv) < 2:
            print("Uso: python clean_data.py <input_csv> [source_pdf] [pdf_date]")
            print("O: python clean_data.py (para ejecutar pruebas)")
            sys.exit(1)
        
        input_csv = sys.argv[1]
        source_pdf = sys.argv[2] if len(sys.argv) > 2 else None
        pdf_date = sys.argv[3] if len(sys.argv) > 3 else None
        
        print(f"Se está procesando el archivo: {input_csv}. Waiting....")
        
        clean_csv(input_csv, source_pdf=source_pdf, pdf_date=pdf_date)
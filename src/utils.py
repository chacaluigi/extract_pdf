from pathlib import Path
from datetime import datetime
import re
from PyPDF2 import PdfReader
import pandas as pd

def ensure_dir(p):
    Path(p).mkdir(parents=True, exist_ok=True)

def parse_date_from_filename(filename: str):
    #intenta extraer fecha YYYYMMDD o YYYY-MM-DD del nombre de archivo.
    m = re.search(r'(\d{4})[-_]?(\d{2})[-_]?(\d{2})', filename)
    if m:
        return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3))).date()
    return None


def normalize_document(doc_text):
    complement=''
    if pd.isna(doc_text):
        return pd.Series(['','',''])
    
    parts=str(doc_text).strip().split('-', 1)

    if parts[0].upper() == 'I':
        doc_type='C.I.'
    elif parts[0].upper() == 'P':
        doc_type='PAS.'
    else:
        doc_type=parts[0]

    doc_number=parts[1]
    
    return pd.Series([doc_type, doc_number, complement]) 

""" def normalize_document(df):
    processed_df=df.copy()
    processed_df["DOCUMENTO"]=processed_df['DOCUMENTO'].str.replace(r'^I\-\s*','', regex=True)
    return processed_df """

from data.dictionary.data_bolivia import BoliviaData
nombres_bolivia = BoliviaData.NOMBRES

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

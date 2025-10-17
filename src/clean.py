import pandas as pd
from pathlib import Path
import sys

DATA_BOL_DIR = Path(__file__).parent.parent
sys.path.insert(0, str(DATA_BOL_DIR))

from data.dictionary.data_bolivia import BoliviaData

nombres_bolivia = BoliviaData.NOMBRES
casos_prueba = BoliviaData.NOMBRES_PRUEBA

def separate_last_and_first_names(text):
    if pd.isna(text):
        return pd.Series(['','',''])
    
    parts=str(text).strip().split()

    if len(parts) < 2:
        print(f'ERROR: EXTRACCIÓN NOMBRE INCORRECTO. El nombre {text} no puede ser menos de 2 palabras.')
        return pd.Series([text, '', ''])
    
    conectors={'de', 'del', 'la', 'tezanos'}
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

def probar_casos_especiales():
    print("PRUEBA DE CASOS ESPECIALES:")
    print("=" * 80)
    for caso in casos_prueba:
        pat, mat, nom = separate_last_and_first_names(caso)
        print(f"ORIGINAL: {caso}")
        print(f"PATERNO:  {pat}")
        print(f"MATERNO:  {mat}") 
        print(f"NOMBRES:  {nom}")
        print("-" * 50)

# Probar la función
probar_casos_especiales()
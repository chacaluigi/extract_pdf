import camelot

def extraer_tablas_camelot(archivo_pdf):
    tablas = camelot.read_pdf(archivo_pdf, pages='2-4')
    
    print(f"Se encontraron {tablas.n} tablas")
    
    for i, tabla in enumerate(tablas):
        print(f"Tabla {i+1}:")
        print(tabla.df)
        print("-" * 50)
    return tablas

# Ejemplo de uso
tablas = extraer_tablas_camelot("src/pdfs/JURADOS+ELECTORALES+COCHABAMBA+2025.pdf")
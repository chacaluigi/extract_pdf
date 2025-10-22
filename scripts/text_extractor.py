import pdfplumber

def extract_dimensions_page(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page = pdf.pages[page_number]
    return page.width, page.height

def extract_pdf_pdfplumber(pdf_file, page_number):
    with pdfplumber.open(pdf_file) as pdf:
        page=pdf.pages[page_number-1]
        #area=page.crop((0, 0, 33, 100))
        area=page.crop((0, 0, 0.33*float(page.width), page.height))
        print(f'ancho: {page.width}, alto: {page.height}')
        im=area.to_image(resolution=150)
        im.save(f"area{page_number}.png", format="PNG")
    return area

#salida=extract_pdf_pdfplumber("data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf")
#print(salida)

w, h = extract_dimensions_page("data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf", 6)
print(f'ancho: {w}, alto: {h}')
a=extract_pdf_pdfplumber("data/raw/2020-10-18-Elecciones-Generales-Cochabamba.pdf", 6)




#area=page.crop((0, 0, 0.33*float(page.width), page.height))

#area=page.crop((0, 0.15*float(page.height), page.width, 0.95*float(page.height)))

""" if end is None or end>total_pages:
            end=total_pages

        if start<0 or start>=total_pages:
            raise ValueError("Start page is out of range.")

        if end<=start:
            raise ValueError("The 'end' value must be greater than 'start'.")
        
        for page_num in range(start, end):
            page=pdf.pages[page_num]
            table=page.extract_table() """

""" def extract_text_pypdf2(pdf_file, start=0, end=None):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        total_pages=len(reader.pages)
        if end is None or end>total_pages:
            end=total_pages
        if start < 0 or start >= total_pages:
            raise ValueError('Start page is out of range.')
        
        if end<=start:
            raise ValueError("The 'end' value must eb greater than 'start'.")

        text = ""

        for page_num in range(start, end):
            page=reader.pages[page_num]
            text+=page.extract_text() or ""
    return text
 """

#texto = extraer_texto_pypdf2("../pdfs/Cochabamba_Lista_EG2V.pdf")
""" text = extract_text_pypdf2("src/pdfs/Cochabamba_Lista_EG2V.pdf",start=2, end=4)

print(text) """
""" def extraer_texto_pdfplumber(archivo_pdf):
    with pdfplumber.open(archivo_pdf) as pdf:
        texto = ""
        for pagina in pdf.pages:
            texto += pagina.extract_text()
    return texto """
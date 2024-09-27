import PyPDF2
import os
import numpy
import pytesseract as tesseract
tesseract.pytesseract.tesseract_cmd = r"C:/Program Files/Tesseract-OCR/tesseract.exe"
import io

#/home/alesson/Documentos/teste/La mujer Bogotá, Colombia, 1895

#files0 = os.listdir('/home/alesson/Documentos/teste/livros')
files0 = os.listdir("C:/Users/Alesson/OneDrive - Universidade de Coimbra/bruto/alema segunda leva organizada ocr/")


files0.sort()
a = numpy.size(files0)
b = a-1
i=0

while b>=0:
    print("quantidade de conversoes",a)
    print("conversao atual",i+1)
    print("convertendo arquivo",files0[i])

    all_files = []
    #for (path, dirs, files) in os.walk('//home/alesson/Documentos/teste/livros/'+files0[i]):
    for (path, dirs, files) in os.walk('C:/Users/Alesson/OneDrive - Universidade de Coimbra/bruto/alema segunda leva organizada ocr/'+files0[i]):
            for file in files:
                if not file.endswith(".jpg"):
                            continue
                file = os.path.join(path,file)
                all_files.append(file)
    pdf_writer = PyPDF2.PdfFileWriter()
    all_files.sort()
# segunda parte    
    for file in all_files:
        page = tesseract.image_to_pdf_or_hocr(file, extension = 'pdf')
        pdf = PyPDF2.PdfFileReader(io.BytesIO(page))
        pdf_writer.addPage(pdf.getPage(0))
    with open(files0[i]+".pdf", "wb") as f:
        pdf_writer.write(f)
    print("converteu",files0[i])
    i=i+1
    b=b-1
print("terminou")
    
    
    
# -*- coding: utf-8 -*-

'''
!pip install pyheif
!pip install img2pdf
!pip install pyheif pillow reportlab
!pip install PyPDF2
'''


import os
import sys
import pyheif
import img2pdf
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from io import BytesIO
import PyPDF2

input_folder = "input/path"

output_folder = "output/path"

def merge_pdfs(pdf_files, output_file):
    merger = PyPDF2.PdfMerger()

    for pdf_file in pdf_files:
        merger.append(pdf_file)

    merger.write(output_file)
    merger.close()

# Function to convert HEIC file to PDF
def convert_to_pdf(input_file, output_file):
    heif_file = pyheif.read(input_file)
    img = Image.frombytes(
        heif_file.mode, 
        heif_file.size, 
        heif_file.data,
        "raw",
        heif_file.mode,
        heif_file.stride,
    )

    # Convert image to JPEG in memory
    img_buffer = BytesIO()
    img.save(img_buffer, format='JPEG')
    img_bytes = img_buffer.getvalue()

    # Convert JPEG bytes to PDF
    pdf_bytes = img2pdf.convert(img_bytes)
    with open(output_file, 'wb') as f:
        f.write(pdf_bytes)

# Find all HEIC files in the input folder
heic_files = [os.path.join(input_folder, f) for f in os.listdir(input_folder) if f.lower().endswith(".heic")]
# define empty space for merged pdf file
pdf_files = []

# Loop through the HEIC files in the input folder and convert HEIC files to PDF
for heic_path in heic_files:
    output_pdf_path = os.path.join(output_folder, os.path.splitext(os.path.basename(heic_path))[0] + ".pdf")
    convert_to_pdf(heic_path, output_pdf_path)
    pdf_files.append(output_pdf_path)

# Merge the PDF files into a single PDF
combined_pdf_path = os.path.join(output_folder, "combined.pdf")
merge_pdfs(pdf_files, combined_pdf_path)


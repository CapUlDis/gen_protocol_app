import re
import io
from PyPDF2 import PdfFileWriter, PdfFileReader
from pathlib import Path
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from datetime import date, datetime

today = date.today()
data_array = []

with open("clb_04000_РП411М.txt") as input_file:
  for line in input_file:
    if line.startswith('Ch'):
      data_array.append(line.rstrip().split(","))

# read your existing PDF

output = PdfFileWriter()

for item in data_array:
  if len(item) == 5:
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont('Times-Bold', 15)
    # название модуля
    can.drawString(270, 623, item[2])
    # серийный номер
    # can.drawString(275, 604, item[1])
    # коэффициент
    can.drawString(353, 532, item[3])
    # смещение
    can.drawString(353, 513, item[4])
    can.drawString(480, 487, today.strftime("%d.%m.%Y"))

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)

    # add the "watermark" (which is the new pdf) on the existing page
    existing_pdf = PdfFileReader(open("РА2.703.047-07 ИНЮ_ПУ1632М4.pdf", "rb"))
    page = existing_pdf.getPage(19)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)

# finally, write "output" to a real file
now = datetime.now().strftime("%d_%m_%y %H_%M_%S")
file_name = f"Протоколы {now}.pdf"
outputStream = open(file_name, "wb")
output.write(outputStream)
outputStream.close()
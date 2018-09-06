# to add blank page with button click
from PyPDF2 import PdfFileWriter, PdfFileReader, PdfFileMerger

file_writer = PdfFileWriter()

file_writer.addBlankPage(height=600,width=1000)

file = open(r"test.pdf","wb")
file_writer.write(file);
file.close()

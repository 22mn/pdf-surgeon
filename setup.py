from cx_Freeze import setup, Executable
from pdfoperator import PdfSetOperator,PdfGetOperator
import sys,tkinter,pdfoperator,os

os.environ["TCL_LIBRARY"]=r"C:\Users\mrmin\AppData\Local\Programs\Python\Python36-32\tcl\tcl8.6";
os.environ["TK_LIBRARY"]=r"C:\Users\mrmin\AppData\Local\Programs\Python\Python36-32\tcl\tk8.6";

include_files = [r"C:\Users\mrmin\AppData\Local\Programs\Python\Python36-32\DLLs\tcl86t.dll",
				r"C:\Users\mrmin\AppData\Local\Programs\Python\Python36-32\DLLs\tk86t.dll"]

base = None

if sys.platform == "win32":
	base = "Win32GUI"

executables = [Executable("pdf-surgeon.py",base=base)]

setup(name="PDF-Surgeon",author="min.naung",options={"build_exe":{"packages":["tkinter"],"include_files":include_files}},
	  version="1.0.0",description="PDF page-editor tool.", executables=executables)
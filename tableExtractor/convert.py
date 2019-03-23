import os
import sys

from win32com import client as wc
w = wc.Dispatch('Word.Application')
w = wc.DispatchEx('Word.Application')
file = "C:\\Users\sadscv\PycharmProjects\gadgets\tableExtractor\docs\cs.doc"
doc=w.Documents.Open(file)

doc.SaveAs(file[:-3]+"docx",16)

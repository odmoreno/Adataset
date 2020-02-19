from tabula import read_pdf
import pandas as pd

import camelot

pdfdir = 'pdfs/1- Sesión 40 del Pleno continuaciónMoción para votación por artículos de la Ley Orgánica de Recursos Hídricos, Usos y Aprovechamiento del Agua.pdf'

df = read_pdf(pdfdir, multiple_tables=True, pages="all")

#print(df)

print(df[1])
df = df[1:]
len = len(df)
cols = df[1].columns.values
cols = cols[1:]
print(cols)

'''
tables = camelot.read_pdf(pdfdir)
print(tables)

tables.export('foo.csv', f='csv', compress=True) # json, excel, html, sqlite
print(tables[0])
print(tables[0].parsing_report)

tables[0].to_csv('foo.csv')
h = tables[0].df
print(h)

'''
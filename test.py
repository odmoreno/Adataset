#Funcion para obtener la información del pdf y sus tablas
from tabula import read_pdf
import pandas as pd
import PyPDF2
import fitz
import camelot


pdfdir = 'pdfs/1.- Sesión 611 del Pleno - Moción Asambleísta Peña forma de debatir Informe Segundo Debate Reformatoria COIP.pdf'
base_dir = 'datasets/'
flag = True
cols = []

def get_dfs(pdfdir):
  df = read_pdf(pdfdir, multiple_tables=True, pages="all")
  print(df[0])
  df = df[1:]
  df = df[:-1]
  return  df

def get_data(pdfdir):
  tables = camelot.read_pdf(pdfdir, pages='all')
  #tables.export('foo.csv', f='csv', compress=True)
  print(tables)
  for table in tables:
    df = table.df
    print(df)
  p = tables[1]
  df = tables[1].df
  a = tables[1].parsing_report
  print(a)
  print('eu')

def concat_dfs(list):
  current_df = list[0]
  current_df = current_df[:-1]
  tmp = list[1:]
  df = None
  for element in tmp:
    element = element[:-1]
    df = pd.concat([current_df, element], axis=0, ignore_index=True)
    current_df = df
    print(df)
  return  df

def get_csv(df):
  tmp = df.drop(columns="Nro.")
  print(tmp)
  path = base_dir + 'dataset.csv'
  tmp.to_csv(path, index=False)


def get_info(pdfdir):
  doc = fitz.open(pdfdir)
  print ("number of pages: %i" % doc.pageCount)
  print(doc.metadata)

  page1 = doc.loadPage(0)
  page1text = page1.getText("text")
  info = page1text.split("\n")
  info = info[1:]
  writeInfo(info)

'''
def get_info2(pdfdir):
  with open(pdfdir, mode='rb') as f:
    reader = PyPDF2.PdfFileReader(f)
    page = reader.getPage(0)
    content = page.extractText()
    tmp = content.split(" ")
    text.append(tmp)
    print(text)
    print(content)
    print(tmp)
'''
def writeInfo(list):
  path = base_dir + 'info.txt'
  with open(path, "w") as output:
    for row in list:
      output.write(str(row) + '\n')
  

if __name__ == "__main__":
  #list = get_dfs(pdfdir)
  #df = concat_dfs(list)
  #print(df)
  #get_csv(df)
  #get_info(pdfdir)
  get_data(pdfdir)
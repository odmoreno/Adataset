from tabula import read_pdf
import pandas as pd
import fitz


class ADataset:

  def __init__(self):
    self.basedir = 'datasets/' #current base dir
    self.pdfdir = None

  def get_dfs(self):
    ''' Obtener las tablas como dataframes'''
    df = read_pdf(self.pdfdir, multiple_tables=True, pages="all") # Obtiene las tablas del pdf como dateframes
    #tmp = df[0] #Informacion general del resumen de la votacion
    #print(tmp)
    df = df[1:] #Eliminamos el resumen de la votacion
    df = df[:-1] # Eliminamos la ultima columna que representa el total presente
    return  df

  def concat_dfs(self, list):
    current_df = list[0] #obtenemos la primera tabla
    current_df = current_df[:-1] #Eliminamos la ultima fila, que representa el total de tal opcion de votacion
    
    tmp = list[1:] # Como tenmos la primera tabla, no la necesitamos mas y la descartamos
    df = None
    for element in tmp:
      element = element[:-1] #Elimina ultima fila
      df = pd.concat([current_df, element], axis=0, ignore_index=True)
      current_df = df
      print(df)
    return  df

  def get_csv(self, df):
    tmp = df.drop(columns="Nro.")
    print(tmp)
    path = self.base_dir + 'dataset.csv'
    tmp.to_csv(path, index=False)
  
  def get_info(self):
    doc = fitz.open(self.pdfdir)
    print ("number of pages: %i" % doc.pageCount)
    print(doc.metadata)

    page1 = doc.loadPage(0) #Resumen de la votacion
    page1text = page1.getText("text")
    info = page1text.split("\n")
    info = info[1:]
    return info 
    #self.writeInfo(info)

  def write_info(self, info):
    path = self.base_dir + 'info.txt'
    with open(path, "w") as output:
      for row in info:
        output.write(str(row) + '\n')
  
  def main(self):
    dfs = self.get_dfs()
    dfconcat = self.concat_dfs(dfs)
    self.get_csv(dfconcat)
    
    info = self.get_info()
    self.writeInfo(info)

  def validate_df(self, df):
    pass

if __name__ == '__main__':
    
    client = ADataset()
    client.pdfdir = 'pdfs/1.- Sesión 611 del Pleno - Moción Asambleísta Peña forma de debatir Informe Segundo Debate Reformatoria COIP.pdf'
    client.main()
    

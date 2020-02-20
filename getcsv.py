from tabula import read_pdf
import pandas as pd
import fitz


class ADataset:

  def __init__(self):
    self.basedir = 'datasets/' #current base dir
    self.pdfdir = None
    self.curulFlag = False
    self.mixFlag = False

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
    current_df = self.validate_df(current_df)
    #current_df = current_df[:-1] #Eliminamos la ultima fila, que representa el total de tal opcion de votacion
    tmp = list[1:] # Como tenmos la primera tabla, no la necesitamos mas y la descartamos
    df = None
    for element in tmp:
      #element = element[:-1] #Elimina ultima fila
      element = self.validate_df(element)
      df = pd.concat([current_df, element], axis=0, ignore_index=True)
      current_df = df
      print(df)
    return  df

  def get_csv(self, df):
    tmp = df.drop(columns="Nro.")
    print(tmp)
    path = self.basedir + 'v1.csv'
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
    path = self.basedir + 'info1.txt'
    with open(path, "w") as output:
      for row in info:
        output.write(str(row) + '\n')
  
  def main(self):
    dfs = self.get_dfs()
    dfconcat = self.concat_dfs(dfs)
    self.get_csv(dfconcat)
    
    info = self.get_info()
    self.write_info(info)

  def validate_df(self, df):
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df.dropna(inplace=True)
    #df = self.validate_last_row(df)
    if not 'Curul' in df.columns: 
      if df.columns[1] != 'Curul':
        name_ = df.columns[1]
        values = df[name_].tolist()
        numm = values[0]
        if numm[0].isdigit(): self.mixFlag = True

      name_ = df.columns[1]
      curul = []
      asambleista = []
      if self.mixFlag:
        name_ = df.columns[1]
        values = df[name_].tolist()
        for value in values:
          v1, v2 = self.validate_num_col((value))
          curul.append(v1)
          asambleista.append(v2)
        self.mixFlag = False
        #self.curulFlag = False
      df['Curul'] = curul
      df['Asambleista'] = asambleista

      del df[name_]
      print(df)
    return df

  def validate_num_col(self, value):
    value = str(value)
    size = len(value)
    num = ''
    name = ''

    if(size <= 2):
      v1 = value[0]
      v2 = v1 + value[1]
      num = v2
      return num, name
    else:
      v1 = value[0]
      v2 = v1 + value[1]
      v3 = v2 + value[2]


    if v1.isdigit():
      if v2.isdigit():
        if v3.isdigit():
          num = v3
          name = value[4:]
        else:
          num = v2
          name = value[3:]
      else:
        num = v1
        name = value[2:]
    return num, name

  def validate_last_row(self, df):
    last = df[-1:]
    #print(cols)
    val = last.values
    val1 = str(val[0][1])
    val2 = str(val[0][3])
    if (val1.lower() == 'nan' ) or (val2.lower() == 'nan'):
      df = df[:-1]

    return df


if __name__ == '__main__':
    
    client = ADataset()
    #client.basedir = '/datasets/'
    client.pdfdir = '1.- Sesión 611 del Pleno - Moción Asambleísta Cedeño plazo 20 días CFCP informe Resolución RL-2019-2021-007 Pleno AN.pdf'
    #client.pdfdir = '1- Sesión 215 del Pleno Archivo de los Proyectos de Ley de Reforma a la Ley Orgánica del Servicio Público.pdf'
    client.main()
    

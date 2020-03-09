from tabula import read_pdf
import pandas as pd
import fitz
from validate import validate_df

class ADataset:

  def __init__(self):
    self.basedir = 'datasets/' #current base dir
    self.pdfdir = None
    self.curulFlag = False
    self.mixFlag = False
    self.sesionName = ''

  def get_dfs(self):
    ''' Obtener las tablas como dataframes'''
    df = read_pdf(self.pdfdir, multiple_tables=True, pages="all") # Obtiene las tablas del pdf como dateframes
    #tmp = df[0] #Informacion general del resumen de la votacion
    #print(tmp)
    df = df[1:] #Eliminamos el resumen de la votacion
    df = df[:-1] # Eliminamos la ultima columna que representa el total presente
    return df

  def concat_dfs(self, list):
    current_df = list[0] #obtenemos la primera tabla
    #current_df = self.validate_df(current_df)
    current_df = validate_df(current_df)
    #current_df = current_df[:-1] #Eliminamos la ultima fila, que representa el total de tal opcion de votacion
    tmp = list[1:] # Como tenmos la primera tabla, no la necesitamos mas y la descartamos
    df = None
    for element in tmp:
      #element = element[:-1] #Elimina ultima fila
      #element = self.validate_df(element)
      element = validate_df(element)
      df = pd.concat([current_df, element], axis=0, ignore_index=True)
      current_df = df
      #print(df)
    return  df

  def get_csv(self, df, name):
    tmp = df.drop(columns="nro.")
    print(tmp)
    path = self.basedir + name + '.csv'
    tmp.to_csv(path, index=False)
  
  def get_info(self, indice):
    doc = fitz.open(self.pdfdir)
    #print("number of pages: %i" % doc.pageCount)
    #print(doc.metadata)
    page1 = doc.loadPage(0) #Resumen de la votacion
    page1text = page1.getText("text")
    info = page1text.split("\n")
    info = info[1:]
    fechaFlag = False
    sesionFlag = False
    totalFlag = False
    presenteFlag =False
    ausenteFlag = False
    siFlag = False
    noFlag = False
    blancoFlag = False
    abstencionFlag = False
    #Datos
    sesion= 0
    asunto= ''
    fecha = ''
    hora = ''
    total = 0
    presente = 0
    ausente = 0
    si = 0
    no = 0
    blanco = 0
    abstencion = 0
    values = []
    for text in info:
      text = text.lower()

      if sesionFlag == True and fechaFlag == False:
        asunto = asunto + text + ' '
        #print(asunto)
      if "sesión" in text:
        #print(text)
        sesion = [int(s) for s in text.split() if s.isdigit()]
        sesion = str(sesion[0])
        #print(sesion[0])
        sesionFlag = True
      if fechaFlag:
        fecha = text
        fecha = fecha[:-5]
        #print(fecha)
        hora = text[-5:]
        #print(hora)
        fechaFlag = False
      if "votación definitiva" in text:
        #print('La sgte contiene la fecha')
        fechaFlag = True
      if totalFlag:
        total = int(text)
        totalFlag = False
      if presenteFlag:
        presente = int(text)
        presenteFlag = False
      if ausenteFlag:
        ausente = int(text)
        ausenteFlag = False
      if siFlag:
        si = int(text)
        siFlag = False
      if noFlag:
        no = int(text)
        noFlag = False
      if blancoFlag:
        blanco = int(text)
        blancoFlag = False
      if abstencionFlag:
        abstencion = int(text)
        abstencionFlag = False
      if text == "total": totalFlag = True
      if text == "presente": presenteFlag = True
      if text == "ausente": ausenteFlag = True
      if text == "si": siFlag = True
      if text == "no": noFlag = True
      if text == "blanco": blancoFlag = True
      if text == "abstencion": abstencionFlag = True

    self.sesionName = 'Sesion_' + sesion + '_v' + str(indice)
    values.append(self.sesionName), values.append(sesion), values.append(asunto), values.append(fecha), values.append(hora), values.append(total), values.append(presente), values.append(ausente)
    values.append(si), values.append(no), values.append(blanco), values.append(abstencion)
    print(values)
    return values


  def write_info(self, info):
    path = self.basedir + 'info1.txt'
    with open(path, "w") as output:
      for row in info:
        output.write(str(row) + '\n')
  
  def main(self, indice):
    dfs = self.get_dfs()
    dfconcat = self.concat_dfs(dfs)
    info = self.get_info(indice)
    
    #self.get_csv(dfconcat)
    #self.write_info(info)

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
    client.pdfdir = '1- Sesión 146 continuaciónVotación - Segundo Debat.pdf'
    #client.pdfdir = '1- Sesión 215 del Pleno Archivo de los Proyectos de Ley de Reforma a la Ley Orgánica del Servicio Público.pdf'
    client.main(0)
    

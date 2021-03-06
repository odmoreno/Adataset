import pandas as pd
import csv


mixFlag = False

votos = ['SI', 'NO', 'BLANCO', 'ABSTENCION', 'AUSENTE']
colsName = ['A1', 'A2', 'valor', 'voto']


def validate_nans(df):
  #df.dropna(inplace=True)
  dftmp = df[df.isnull().any(axis=1)]
  print(dftmp)
  if dftmp.size > 0 :
    df.dropna(inplace=True)
    return df
  else:
    return df

def validate_num_col(value):
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

def validate_rows(df):
  #print(df)
  cols = ['nro.', 'curul', 'asambleista', 'voto']
  dfcols = df.columns.values
  df.columns = map(str.lower, df.columns)
  dfcols = [x.lower() for x in dfcols]
  s = set(dfcols)
  #matches = [j for i, j in zip(cols, dfcols) if i != j]
  matches = [x for x in s if x not in cols]
  matches = [y.lower() for y in matches]
  print('matches: ')
  print(matches)
  curul = []
  asambleista = []
  if len(matches) > 0:
    print('Errores en columnas')
    nameErr = 'curul asambleista'
    if nameErr in matches:
      print('contains curul asambleista')
      values = df[nameErr].tolist()
      for value in values:
        v1, v2 = validate_num_col(value)
        curul.append(v1)
        asambleista.append(v2)

      df['curul'] = curul
      df['asambleista'] = asambleista
      del df[nameErr]

    #print(df)
    return df
  
  return df

def validate_df(df):
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
  df = validate_nans(df)
  df = validate_rows(df)
  return df


def create_df(pathSesion):
  votos = ['SI', 'NO', 'BLANCO', 'ABSTENCION', 'AUSENTE']
  colsName = ['A1', 'A2', 'voto', 'valor']

  df = pd.read_csv(pathSesion)
  df = df[['asambleista', 'curul', 'voto']]

  colVotos = df['voto']
  tmpDf = pd.DataFrame(columns=colsName)

  dict = {}
  count = 0
  for voto in votos:
    if voto in colVotos.values:
      votoDf = df.loc[df['voto'] == voto]
      lol = votoDf.values.tolist()
      for index, this in enumerate(lol):
        for that in lol[index + 1:]:
          info = [this[0], that[0], this[2], 1]
          tmpDf = tmpDf.append(pd.Series(info, index=colsName), ignore_index=True)
          dict[count] = info
          count +=1
          #print('this: ' + this[0] + ' that: ' + that[0])
      print(tmpDf)
    else:
      print('No hay votos con: ' + voto)

  return tmpDf, dict

def create_zeros(df, tam):

  for i in range(0, tam):
    tmp = pd.DataFrame({"A1": 'test', "A2": 'test', "voto": 'test', "valor": [0]})
    df = df.append(tmp, ignore_index=True)

  return df

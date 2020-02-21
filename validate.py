import pandas as pd

mixFlag = False
curul = []
asambleista = []


def validate_nans(df):
  #df.dropna(inplace=True)
  dftmp = df[df.isnull().any(axis=1)]
  print(dftmp)
  pass

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

def validate_rows(df):
  cols = ['nro.', 'curul', 'asambleista', 'voto']
  dfcols = df.columns.values
  dfcols = [x.lower() for x in dfcols]
  s = set(dfcols)
  #matches = [j for i, j in zip(cols, dfcols) if i != j]
  matches = [x for x in s if x not in cols]
  matches = [y.lower() for y in matches]
  print(matches)
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
    
    df['Curul'] = curul
    df['Asambleista'] = asambleista
    del df[nameErr]
    print(df)
    return df
  
  return df

def validate_df(df):
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
  validate_nans(df)
  #df = validate_nans(df)
  df = validate_rows(df)
  return df
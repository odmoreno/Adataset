import pandas as pd

def validate_nans(df):
  pass

def validate_df(self, df):
  df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
  df.dropna(inplace=True)
  #df = validate_nans(df)
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
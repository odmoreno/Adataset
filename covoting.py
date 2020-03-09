import os
import getcsv
import pandas as pd

datafolder = 'datasets'
testfile =  'datasets/Sesion 0_v0.csv'
basedir = 'votos/'
nameCsv = 'votos_0_v0.csv'

#asambleistas
nodes = {}
# enlaces
links = {}

votos = ['SI', 'NO', 'BLANCO', 'ABSTENCION', 'AUSENTE']
colsName = ['A1', 'A2', 'valor', 'voto']
sesDf = pd.DataFrame(columns=colsName)


df = pd.read_csv(testfile)
col = df['voto']
tmpvotos = votos


for index, row in df.iterrows():
    #print(row['asambleista'], row['voto'])
    list = [row['asambleista'], row['voto']]
    nodes[row['asambleista']] = index
    #print(nodes)


for voto in tmpvotos:
    if voto in col.values:
        votoDf = df.loc[df['voto'] == voto]
        lol = votoDf.values.tolist()
        for index, this in enumerate(lol):
            for that in lol[index + 1:]:
                info = [this[0], that[0], 1, this[2]]
                # actualList.append(list)
                sesDf = sesDf.append(pd.Series(info, index=colsName), ignore_index=True)
                print('this: ' + this[0] + ' that: ' + that[0])

        print(sesDf)
    else:
        print('No hay votos con: ' + voto)


path = basedir + nameCsv
sesDf.to_csv(path, index=False)
print('fin')



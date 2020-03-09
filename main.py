import os
import pandas as pd
import numpy as np
import csv

import  validate

datafolder = 'datasets/'
basedir = 'votos/'

firstFlag = True
dictflag = True

colsName = ['A1', 'A2', 'voto', 'valor']
sesDf = pd.DataFrame(columns=colsName)
lastdict = {}

def writeCsv(dict, name):
    path = basedir + name
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file)
        items = dict.items()
        writer.writerow(colsName)
        for key, link in items:
            writer.writerow(link)


def compareDf(df1, df2, currentD, dictflag):
    idf = pd.merge(df1, df2, how='inner')
    items = currentD.items()
    for index, row in idf.iterrows():
        a1 = row['A1']
        a2 = row['A2']
        for key, link in items:
            aa1 = link[0]
            aa2 = link[1]
            if a1 == aa1 and a2 == aa2:
                print(key)
                if dictflag:
                    valor = link[3] + 1
                    list = [aa1, aa2, link[2], valor]
                else:
                    print('Key: ' + str(key))
                    if key in lastdict:
                        print('Existe')
                        v1 = lastdict[key]
                        valor = v1[3] + 1
                        list = [aa1, aa2, link[2], valor]
                    else:
                        print('No existe registro ')
                        valor = link[3]
                        list = [aa1, aa2, link[2], valor]

                currentD[key] = list
                print(currentD[key])

    dictflag = False
    print('test line')
    return currentD, dictflag


for folderName, subfolders, filenames in os.walk(datafolder):
    print(filenames)
    filenames.sort()
    for file in filenames:
        dpath = datafolder + file
        codf, dict = validate.create_df(dpath)

        if firstFlag:
            sesDf = codf
            #lastdict = dict
            firstFlag = False
            newfile = 'cv_' + file
            path = basedir + newfile
            sesDf.to_csv(path, index=False)
        else:
            newdict, flag = compareDf(sesDf, codf, dict, dictflag)
            sesDf = codf
            lastdict = newdict
            dictflag = flag
            newfile = 'cv_' + file
            writeCsv(newdict, newfile)

    print('test end line')
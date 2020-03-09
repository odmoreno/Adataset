import os
import getcsv
import pandas as pd

pdfsfolder = 'pdfs/'
csvs = getcsv.ADataset()
currentsession = ''
indiceName = 'sesiones.csv'

colNames = ['titulo', 'sesion', 'fecha', 'hora', 'total', 'presente', 'ausente', 'si', 'no', 'blanco', 'abstencion', 'asunto']
sesDf = pd.DataFrame(columns=colNames)


for folderName, subfolders, filenames in os.walk(pdfsfolder):
  for folder in subfolders:
    path = os.path.join(folderName, folder)
    for foldern2, subf2, fnames2 in os.walk(path):
      for folder2 in subf2:
        path2 = os.path.join(foldern2, folder2)
        for foldern3, subf3, fnames3 in os.walk(path2):
          for folder3 in subf3:
            path3 = os.path.join(foldern3, folder3)
            for folder4, subf4, filenames4 in os.walk(path3):
              print(filenames4)
              count = 0
              for files in filenames4:
                path4 = os.path.join(folder4, files)
                print(path4)
                csvs.pdfdir = path4
                try:
                  dfs = csvs.get_dfs()
                  dfconcat = csvs.concat_dfs(dfs)
                  info = csvs.get_info(count)
                  name = csvs.sesionName
                  csvs.get_csv(dfconcat, name)
                  sesDf = sesDf.append(pd.Series(info, index=colNames), ignore_index=True)
                except Exception as e:
                  print(e)
                  raise e
                count += 1


print(sesDf)
path = csvs.basedir + indiceName
sesDf.to_csv(path, index=False)
import numpy as np


dictionary = {
    '1' : ['a1', 'a2', 'si', 1], '2' : ['a1', 'a3', 'no', 1]}
items = dictionary.items()
for key, link in items:    # for name, age in dictionary.iteritems():  (for Python 2.x)
    a1 = link[0]
    a2 = link[1]
    if a1 == 'a1' and a2 =='a2':
        print(key)

'''
if sizeI == df1.size:
    idf['valor1'] = np.where((idf['A1'] == df1['A1']) & (idf['A2'] == df1['A2']), df1['valor'] + idf['valor'], 0)
    print(idf)
elif sizeI == df2.size:
    idf['valor1'] = np.where((idf['A1'] == df2['A1']) & (idf['A2'] == df2['A2']), df2['valor'] + idf['valor'], 0)
    print(idf)
'''

'''

    shapeD1 = df1.shape
    shapeD2 = df2.shape

    if shapeD1[0] < shapeD2[0]:
        dif = shapeD2[0] - shapeD1[0]
        newdf1 = validate.create_zeros(df1, dif)

    tmp2 = df2
    tmp2['valor'] = np.where((newdf1['A1'] == tmp2['A1']) & (newdf1['A2'] == tmp2['A2']), newdf1['valor'] + tmp2['valor'], 0)
    print('OHH')

    df = pd.merge(df2, df1, how="outer", indicator=True)
    df = df[df['_merge'] == 'left_only']
    del df['_merge']

    newdf = pd.merge(df, idf, how='outer')

    antdf = pd.merge(df1, df2, how="outer", indicator=True)
    antdf = antdf[antdf['_merge'] == 'left_only']
    del antdf['_merge']

    backup = pd.merge(antdf, newdf, how='outer')

    
'''
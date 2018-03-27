# coding=utf-8
import pandas as pd


def get_csv(file_name):

    # df = pd.read_csv(file_name, header=None, names=['File', 'NP', 'MDD', 'PpT', 'MDD_iC', 'LVRG',
    #                                                 'LVRG_Mon_NP', 'TT', 'ShR', 'NumD'])

    df = pd.read_csv(file_name)
    # t = df.sort_values(by='NP')

    # print t['NP']
    # print t['NP']
    t = df.sort_values(by='LVRG', ascending=False).head(10)
    print type(df)
    # print df['NP'][1]
    print t['NP']
    print t['LVRG']


def test_unit1(file_name):

    storage_csv = []

    data_csv = pd.read_csv(file_name)
    LVRG_data = data_csv.sort_values(by='LVRG', ascending=False)[0:100]
    LVRG_Mon_NP_data = data_csv.sort_values(by='LVRG_Mon_NP', ascending=False)[0:100]
    NP_data = data_csv.sort_values(by='NP', ascending=False)[0:100]
    ShR_data = data_csv.sort_values(by='ShR', ascending=False)[0:100]
    ### merge

    temp_data = [LVRG_data['File'], LVRG_Mon_NP_data['File'], NP_data['File'], ShR_data['File']]
    # for i in range(1, len(temp_data[0])):
    #    storage_csv.append(temp_data[0][i])

    for i in temp_data[0]:
        storage_csv.append(i)
    # 合并的操作

    for i in range(1, len(temp_data)):
        for j in temp_data[i]:
            if j not in storage_csv:
                storage_csv.append(j)

    sort_data = pd.merge(LVRG_Mon_NP_data, NP_data, on='File')
    sort_data = pd.merge(sort_data, ShR_data, on='File')
    # sort_data = pd.merge(sort_data, LVRG_data, on='File')
    sort_name = sort_data['File']
    # print ShR_data[:10]
    # print len(sort_data)
    print len(storage_csv)

    return storage_csv

# get_csv('newfile/0indicator_statistics.csv')
test_unit1('newfile/0indicator_statistics.csv')


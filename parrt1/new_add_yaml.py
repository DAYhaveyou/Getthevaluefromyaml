# coding=utf-8

import MySQLdb as mdb
import get_yaml as yl
import os
import time
import yaml
import test_db


def connect():
    conn = mdb.connect(host='10.25.10.249', user='huacheng', passwd='huacheng', db='huacheng')
    sql = 'show tables'
    cursor = conn.cursor()
    cursor.excute(sql)

    val = cursor.fetchall()

    conn.close()
    print val


def test_unit():
    dir_name = ''
    file_names = os.listdir(dir_name)
    yaml_file = ""

    file_num = 0

    # f_yaml = open(yaml_file)
    print "Please wait to get the yaml data! name:\t %s" % yaml_file
    g_t1 = time.time()
    f_value = open(yaml_file)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    g_all_length = len(raw_values)
    for i in range(g_all_length):
        value_temp = yl.deal_val_strategy(raw_values[i])
        if value_temp[10] in file_names:
            file_num += 1
    print file_num


def test_unit1(table, message):
    '''
    dir_name1 = '/home/liziqiang/Desktop/SHOWyou/j_zs_WH_WOBV_DX_QG_GZ_20180102-81542_grid.yaml'
    file_names = os.listdir(dir_name1)
    yaml_file = ""

    file_num = 0
    is_yaml = 0
    print "1 is ok"
    for file_s in file_names:
        if '.yaml' in file_s:
            print file_s[-5:]
            yaml_file = file_s
            is_yaml = 1
            break

            # f_yaml = open(yaml_file)
    print yaml_file
    print file_names[0]
    print len(file_names)
    
    yaml_file = dir_name1+'/'+yaml_file
    if is_yaml == 0:
        print "can't find the yaml file"
        return
    '''
    yaml_file = "5PP5LY1.yaml"
    print "Please wait to get the yaml data! name:\t %s" % yaml_file
    g_t1 = time.time()
    f_value = open(yaml_file)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    g_all_length = len(raw_values)

    for i in range(2, g_all_length):
        # g_t3 = time.time()
        # value_temp = yl.deal_val_strategy(raw_values[i])
        value_temp = yl.deal_val_strategy(raw_values[i])
        if len(value_temp) < 11:
            print "Wrong!"
            return
        temp_id = test_db.insert_yaml(table, message, value_temp)

        # g_t4 = time.time()
        # print "Num %d cost %f s" % (temp_id, (g_t4 - g_t3))
        # print "Num ", temp_id, " cost ", (g_t4 - g_t3), "s"
        # if value_temp[10] in file_names:
        #    file_num += 1
    # print "The total file number: ", file_num


def test_unit3():
    yaml_file = "5PP5LY1.yaml"
    print "Please wait to get the yaml data! name:\t %s" % yaml_file
    g_t1 = time.time()
    f_value = open(yaml_file)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    g_all_length = len(raw_values)
    '''
    val = yl.deal_val_strategy(raw_values[178])

    for i in val:
        print i

    val1 = yl.deal_val_strategy(raw_values[179])
    for i in val1:
        print i
    '''

    val2 = yl.deal_val_strategy(raw_values[181])
    test_db.insert_yaml(table1, message1, val2)
    for i in val2:
        print i
    print raw_values[181][2]['Optimum']


# 头部信息参数
def test_head_information(val1, val2):
    Data_Table = val1['Data']['Table']
    Data_Symbol_CommissionRatio = val1['Data']['Symbol']['CommissionRatio']
    Data_Symbol_Market = val1['Data']['Symbol']['Market']
    Data_Symbol_MktDataType = val1['Data']['Symbol']['MktDataType']
    Data_Symbol_Trade = val1['Data']['Symbol']['Trade']

    Setting_BktVfy = val2['Setting']['BktVfy']
    Setting_Objective_Fitness = val2['Setting']['Objective']['Fitness']
    Setting_Objective_ObjInSam = val2['Setting']['Objective']['ObjInSam']
    Setting_Objective_ObjOutSam = val2['Setting']['Objective']['ObjOutSam']
    Setting_Objective_ObjVldSam = val2['Setting']['Objective']['ObjVldSam']
    Setting_Objective_ScoreFormula = val2['Setting']['Objective']['ScoreFormula']
    Setting_OptCont = val2['Setting']['OptCont']
    Setting_OptEngine_SPSO_Epsilon = val2['Setting']['OptEngine']['SPSO']['Epsilon']
    Setting_OptEngine_SPSO_EvalMax = val2['Setting']['OptEngine']['SPSO']['EvalMax']
    Setting_OptEngine_SPSO_RunMax = val2['Setting']['OptEngine']['SPSO']['RunMax']
    Setting_OptResultSize = val2['Setting']['OptResultSize']
    Setting_SamRange_InSamStart = val2['Setting']['SamRange']['InSamStart']
    Setting_SamRange_OutSamRangeMonth = val2['Setting']['SamRange']['OutSamRangeMonth']
    Setting_SamRange_OutSamStart = val2['Setting']['SamRange']['OutSamStart']
    Setting_TradeLots = val2['Setting']['TradeLots']

    return Data_Table, Data_Symbol_CommissionRatio, Data_Symbol_Market, Data_Symbol_Market, \
           Data_Symbol_MktDataType, Data_Symbol_Trade, Setting_BktVfy, Setting_Objective_Fitness, \
           Setting_Objective_ObjInSam, Setting_Objective_ObjOutSam, Setting_Objective_ObjVldSam, \
           Setting_Objective_ScoreFormula, Setting_OptCont, Setting_OptEngine_SPSO_Epsilon, \
           Setting_OptEngine_SPSO_EvalMax, Setting_OptEngine_SPSO_RunMax, Setting_OptResultSize,\
           Setting_SamRange_InSamStart, Setting_SamRange_OutSamRangeMonth, Setting_SamRange_OutSamStart, \
           Setting_TradeLots


def get_head():
    f = open('yaml_head.yaml')
    raw_val = yaml.load(f)
    f.close()
    print raw_val[2][0]
    print raw_val[2][1]
    print raw_val[2][2]


def load_head(val):
    f = open("yaml1_self.yaml", 'w')
    yaml.dump(val, f)
    f.close()


def do_head_new_yaml(val1, val2):
    # 1
    dict_data = {}
    dict_data['Data'] = ""
    dict_data_database_d = {}
    dict_data_database_d["DataBase"] = ""
    dict_data_database = {}
    dict_data_database['DB'] = "huacheng"  # 1
    dict_data_database['PassWd'] = "huacheng123"
    dict_data_database['Server'] = "10.25.10.249"
    dict_data_database['Table'] = ['rb_zs']
    dict_data_database['User'] = "huacheng"
    dict_data_database_d["DataBase"] = dict_data_database

    dict_data_symbol_dict = {}
    dict_data_symbol_dict["CommissionRatio"] = "n"
    dict_data_symbol_dict["Market"] = "RB"
    dict_data_symbol_dict["MktDataType"] = "KBar"
    dict_data_symbol_dict["Trade"] = "RB"
    dict_data_database_d["Symbol"] = dict_data_symbol_dict

    dict_data['Data'] = dict_data_database_d

    # 2
    dict_setting = {}
    dict_setting['Setting'] = ""

    dict_setting_val = {}
    dict_setting_val['BktVfy'] = "n"
    dict_setting_val['Objective'] = {}
    dict_setting_val['Objective']['Fitness'] = [['LVRG_Mon_NP', 0.2, 0], ['NP', 0]]
    dict_setting_val['Objective']['ObjInSam'] = [['DD/Close', 1.2]]
    dict_setting_val['Objective']['ObjOutSam'] = [['NP', 100000]]
    dict_setting_val['Objective']['ObjVldSam'] = [['NP/-MDD', 0.5]]
    dict_setting_val['Objective']['ScoreFormula'] = "LVRG_Mon_NP"
    dict_setting_val['OptCont'] = "n"
    dict_setting_val['OptEngine'] = {}
    dict_setting_val['OptEngine']["SPSO"] = {}
    dict_setting_val['OptEngine']["SPSO"]['Epsilon'] = 0.0010
    dict_setting_val['OptEngine']["SPSO"]['EvalMax'] = 100
    dict_setting_val['OptEngine']["SPSO"]['RunMax'] = 2
    dict_setting_val['OptResultSize'] = 5
    dict_setting_val['SamRange'] = {}
    dict_setting_val['SamRange']['InSamStart'] = 20140101
    dict_setting_val['SamRange']['OutSamRangeMonth'] = 3
    dict_setting_val['SamRange']['OutSamStart'] = 20170101
    dict_setting_val['TradeLots'] = 10
    dict_setting['Setting'] = dict_setting_val

    # 3
    dict_3_values = []
    dict_3_values[0] = {}
    dict_3_values[0]['Strategy'] = "1"

    dict_3_values[1] = {}
    dict_3_values[1]['Config'] = {}
    dict_3_values[1]['Config']['Parameters'] = []
    dict_3_values[1]['Config']['WarmUp'] = -10000
    dict_3_values[1]['Config']['KBarPeriod'] = {}
    dict_3_values[1]['Config']['KBarPeriod']['KBarTimeMin'] = 13

    dict_3_values[2] = {}
    dict_3_values[2]['Optimum'] = []

    vals = []
    vals.append(dict_data)
    vals.append(dict_setting)
    vals.append(dict_3_values)
    f1 = open("test_head.yaml", 'w')

    yaml.dump(vals, f1)

    f1.close()

    print vals


def create_all_names(table, message):
    sql = "create table %s (specie_id int not null AUTO_INCREMENT," \
          "specie_name VARCHAR(100) not null," \
          "specie_table_name VARCHAR(100) not null," \
          "import_time TIMESTAMP  DEFAULT CURRENT_TIMESTAMP()," \
          "import_operator VARCHAR(36) NOT NULL DEFAULT 'Likeyo'," \
          "DB VARCHAR(100) NOT NULL," \
          "PassWd VARCHAR(50) NOT NULL," \
          "Server VARCHAR(60) NOT NULL," \
          "Tablename VARCHAR(60) NOT NULL," \
          "DB_User VARCHAR(60) NOT NULL," \
          "Symbol_CR VARCHAR(10) NOT NULL," \
          "Symbol_M VARCHAR(30) NOT NULL," \
          "Symbol_MDT VARCHAR(30) NOT NULL," \
          "Symbol_T VARCHAR(30) NOT NULL," \
          "Setting_BV VARCHAR(10) NOT NULL," \
          "Setting_OBJ_Fitness TintText NOT NULL," \
          "Setting_OBJ_insam VARCHAR(100) NOT NULL," \
          "Setting_OBJ_outsam VARCHAR(100) NOT NULL," \
          "Setting_OBJ_vlsam VARCHAR(100) NOT NULL," \
          "Setting_OBJ_SF VARCHAR(60) NOT NULL," \
          "Setting_OptCont VARCHAR(10) NOT NULL," \
          "Setting_OE_SPSO_E FLOAT NOT NULL," \
          "Setting_OE_SPSO_EM FLOAT NOT NULL," \
          "Setting_OE_SPSO_RM FLOAT NOT NULL," \
          "Setting_ORS int NOT NULL," \
          "Setting_SamRange_inSS int NOT NULL," \
          "Setting_SamRange_outSRangeMonth int NOT NULL," \
          "Setting_SamRange_outSS int NOT NULL," \
          "Setting_TradeLots int NOT NULL," \
          "PRIMARY KEY (specie_id))"

    pass


table1 = 'yaml_table'
message1 = ['127.0.0.1', 'root', '7ondr', 'testpy']

head_val = [{'Data': {'Symbol': {'MktDataType': 'KBar', 'CommissionRatio': 'n', 'Market': 'RB', 'Trade': 'RB'}, 'DataBase': {'PassWd': 'huacheng123', 'Table': ['rb_zs'], 'DB': 'huacheng', 'User': 'huacheng', 'Server': '10.25.10.249'}}}, {'Setting': {'SamRange': {'InSamStart': 20140101, 'OutSamStart': 20170101, 'OutSamRangeMonth': 3}, 'OptResultSize': 5, 'TradeLots': 10, 'Objective': {'ScoreFormula': 'LVRG_Mon_NP', 'ObjVldSam': [['NP/-MDD', 0.5]], 'Fitness': [['LVRG_Mon_NP', 0.2, 0], ['NP', 0]], 'ObjOutSam': [['NP', 100000]], 'ObjInSam': [['DD/Close', 1.2]]}, 'OptEngine': {'SPSO': {'Epsilon': 0.001, 'RunMax': 2, 'EvalMax': 100}}, 'OptCont': 'n', 'BktVfy': 'n'}}]

# test_unit1(table1, message1)
# test_unit3()

# print float('inf')
# a = [float('inf')]
# print a[0]*float('-inf')
# get_head()
# load_head(head_val)
# do_head()


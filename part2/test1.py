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

table1 = 'yaml_table'
message1 = ['127.0.0.1', 'root', '7ondr', 'testpy']
# test_unit1(table1, message1)
# test_unit3()

# print float('inf')
# a = [float('inf')]
# print a[0]*float('-inf')



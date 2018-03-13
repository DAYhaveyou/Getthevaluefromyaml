# coding=utf-8

import MySQLdb as mdb
import get_yaml as yl
import os
import time
import yaml


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


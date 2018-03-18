# coding=utf-8
import time
import datetime
import MySQLdb as mdb
import numpy as np
import sys
import os
import test6
import get_index
import yaml
import get_yaml as yl
import test_db


def connect_database_test(message):
    host_id, user_name, password, db_name = message
    conn = mdb.connect(host=host_id, user=user_name, passwd=password, db=db_name)
    return conn


# 创建基础筛选csv的指标
def create_names_table_test(name, table_f, message):
    conn = connect_database_test(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql = "create table %s(name_id int not null AUTO_INCREMENT," \
          "name varchar(200) not null," \
          "NP FLOAT DEFAULT 0.0," \
          "MDD  FLOAT DEFAULT 0.0," \
          "mDD_mC FLOAT DEFAULT 0.0," \
          "mDD_iC FLOAT DEFAULT 0.0," \
          "LVRG FLOAT DEFAULT 0.0," \
          "LVRG_Mon_NP FLOAT DEFAULT 0.0," \
          "PpT  FLOAT DEFAULT 0.0," \
          "TT FLOAT DEFAULT 0.0," \
          "ShR  FLOAT DEFAULT 0.0," \
          "Days FLOAT DEFAULT 0.0," \
          "D_WR FLOAT DEFAULT 0.0," \
          "D_STD FLOAT DEFAULT 0.0," \
          "D_MaxNP FLOAT DEFAULT 0.0," \
          "D_MinNP FLOAT DEFAULT 0.0," \
          "maxW_Days FLOAT DEFAULT 0.0," \
          "maxL_Days FLOAT DEFAULT 0.0," \
          "stop_loss FLOAT DEFAULT 20," \
          "point_value FLOAT DEFAULT 5," \
          "origin_insert_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()," \
          "change_select_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP()," \
          "origin_operator VARCHAR(36) DEFAULT 'Likeyo'," \
          "select_operator VARCHAR(36) DEFAULT 'NO_ONE'," \
          "fcsv_id int not null DEFAULT 0," \
          "PRIMARY KEY (name_id)," \
          "constraint FK_fcsv_id foreign key(fcsv_id) references %s(csv1_id))" % (name, table_f)

    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# build the table that related with names table
def create_yaml_table_test(table, message):

    sql1 = "create table "+table+"(csv1_id int not null AUTO_INCREMENT," \
                                 "strategy varchar(100) not null," \
                                 "Config_WarmUp float not null," \
                                 "Config_KBarPeriod_KBarTimeMin int not null," \
                                 "Config_Parameters text not null," \
                                 "optimum_num int not null," \
                                 "optimum_period varchar(100) not null," \
                                 "optimum_values text not null," \
                                 "back_test_num int not null," \
                                 "back_test_period varchar(100) not null," \
                                 "back_test_value text not null," \
                                 "csv_name varchar(200) not null," \
                                 "PRIMARY KEY (csv1_id))"
    conn = connect_database_test(message)
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit()
    conn.close()


# add a all names
def create_all_name(table, message):
    sql = ""
    pass


# 进行删选的时候需要使用进行信息加入
def update_user_name_and_change_time(table, message, values):
    stop_loss, point_value, select_operator = values
    now = datetime.datetime.now()
    change_select_time = now.strftime("%Y-%m-%d %H:%M:%S")
    values = [stop_loss, point_value, select_operator, change_select_time]

    conn = connect_database_test(message)
    cursor = conn.cursor()

    try:
        sql = "update "+table+" set stop_loss=%s, point_value=%s, select_operator=%s, change_select_time=%s where " \
                              "name_id=%s"
        cursor.execute(sql, values)

    except Exception:
        print "Execute failed!"
    conn.commit()
    cursor.close()
    conn.close()


message_test = ['127.0.0.1', 'root', '7ondr', 'testpy']
table1 = 'test_basic_yaml'
table2 = 'test_name_1'

# create_yaml_table_test(table1, message_test)
create_names_table_test(table2, table1, message_test)


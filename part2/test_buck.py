# coding=utf-8
import time
import MySQLdb as mdb
import numpy as np
import sys
import os
import test6
import get_index
import yaml
import get_yaml as yl
import test_db
import for_all_specie_manage as fm

'''part 0'''
# The comment
'''
(!*_*!) show you are pig!
(!-_-!) show not good!
(-_-) show normal!
(^_^) show good!
(\^_^/) show perfect!
'''


'''part 1'''


# just for test
def storage_value(table_name):

    if 2 != len(sys.argv):
        exit(-1)

    dir_name = sys.argv[1]
    file_names = os.listdir(dir_name)
    for file in file_names:
        if file[-4:] == '.csv':
            s = file
            val1, val2, val3, val4, val5, val6, val7, val8 \
                = np.loadtxt("%s" % s, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True)
            # values = [val1, val2, val3, val4, val5, val6, val7, val8]
    for i in range(len(val1[:10])):
        values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
        insert_values(values, table_name)

'''
def insert_values(values, table_name):
    conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql1="insert into "+table_name+"(a, b, c1, d, e, f, g, h) values("+str(values[0])+","+str(values[1])+","+str(values[2])+","+str(values[3])+","+str(values[4])+","\
    +str(values[5]) + ","+str(values[6])+","+str(values[7])+")"
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit()
    conn.close()
'''


def connect_database(message):
    host_id, user_name, password, db_name = message
    conn = mdb.connect(host=host_id, user=user_name, passwd=password, db=db_name)
    return conn


'''part 2'''


# a way to deal name (-_-)
def deal_name(name):
    le = len(name)
    file_name = name
    str1 = ''
    site = 0
    for i in range(le):
        if name[i] == '.':
            str1 = file_name[:i]
            site = i+1
            break

    # le1 = len(file_name)
    for i in range(site, le):
        if name[i] == "K":
            if name[i:i+4] == 'KBar':
                str1 += file_name[i:-4]
    return str1.replace('-', '_')


# (-_-)
def storage_name(name, table_name, message, c_id=0):
    sql = "insert into %s(name1, fcsv_id) VALUES('%s', %d) " % (table_name, name, c_id)
    print sql
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# use for name
# get the stop loss and point value
def get_name_stoploss_pointvalue(table, message):
    sql = "select name1, stop_loss, point_value from %s" % table
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    cursor = conn.cursor()
    cursor.execute(sql)
    val = []
    values = cursor.fetchall()
    # print values
    for i in range(len(values)):
        val.append(values[i])
    # val1 = list(values)
    # print val
    conn.close()
    return val


# just get_name
def get_name(table, message):
    sql = "select name1 from %s" % table
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    cursor = conn.cursor()
    cursor.execute(sql)
    val = []
    values = cursor.fetchall()
    # print values
    for i in range(len(values)):
        val.append(values[i][0])
    # val1 = list(values)
    # print val
    conn.close()
    return val


def csv_to_database(message):
    '''
    if 2 != len(sys.argv):
        exit(-1)
    '''
    t = time.time()
    dir_name = 'H:\PYFILE\Tf\j9000'
    file_names = os.listdir(dir_name)
    t2 = 0
    for file in file_names:
        if file[-4:] == '.csv':
            s = dir_name + '\\' + file
            name = file[:-4]
            name1 = deal_name(name)
            print name1
            create_table(name1, message)
            storage(name1, s, message)
            storage_name(name1, 'names', message)
            t1 = time.time() - t
            print t2, t1
            t2 += 1


def yaml_to_database(message, dir_name):
    file_names = os.listdir(dir_name)  # get the file names in dir_name


def get_raw_data(table_all, dir_name, table, table2, message):
    is_yaml = 0
    file_name = ""
    file_names = os.listdir(dir_name)  # get the file names in dir_name
    # just ready for a file have one yaml file, if need more Please find all
    for file_s in file_names:
        if file_s[-5:] == '.yaml':
            file_name = file_s
            is_yaml = 1
            break
    if is_yaml == 0:
        return
    print file_name
    print 'success!'

    '''
    here need a name to make sure the single sort!
    '''
    file_temp_name = file_name  # 将要存储的文件
    file_name = dir_name+'/'+file_name
    print "Please wait to get the yaml data! name:\t %s" % file_name
    g_t1 = time.time()
    f_value = open(file_name)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    '''
    在这里需要加一个进行全局管理的函数将names 和 yaml 存入其中
    同时 这两者的名字处理需要设定标准
    '''

    fm.storage_values_specie(table_all, table, table2, 'Likeyo', message, file_name)
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    raw_values = raw_values
    g_all_length = len(raw_values)
    # print g_all_length
    print "Now read the data to move to database."
    for i in range(2, g_all_length):
        value_temp = yl.deal_val_strategy(raw_values[i])
        temp_id = test_db.insert_yaml(table2, message, value_temp)
        print "The insert value's csv_file name: %s " % value_temp[10]  # 0 1 2 3 4 5 6 7 8 9 10
        if value_temp[10] in file_names:
            s = dir_name+'/' + value_temp[10]
            name = value_temp[10][:-4]
            name1 = deal_name(name)
            print name1
            create_table(name1, message)
            storage(name1, s, message)
            storage_name(name1, table, message, temp_id)
    insert_index_names_16(table, message)


def get_raw_data_selected_good(table_all, dir_name, table, table2, message, file_name_vals):
    is_yaml = 0
    file_name = ""
    file_names = os.listdir(dir_name)  # get the file names in dir_name
    # just ready for a file have one yaml file, if need more Please find all
    for file_s in file_names:
        if file_s[-5:] == '.yaml':
            file_name = file_s
            is_yaml = 1
            break
    if is_yaml == 0:
        return
    print file_name
    print 'success!'

    '''
    here need a name to make sure the single sort!
    '''
    file_temp_name = file_name  # 将要存储的文件
    file_name = dir_name+'/'+file_name
    print "Please wait to get the yaml data! name:\t %s" % file_name
    g_t1 = time.time()
    f_value = open(file_name)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    '''
    在这里需要加一个进行全局管理的函数将names 和 yaml 存入其中
    同时 这两者的名字处理需要设定标准
    '''

    fm.storage_values_specie(table_all, table, table2, 'Likeyo', message, file_name)
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    raw_values = raw_values
    g_all_length = len(raw_values)
    # print g_all_length
    print "Now read the data to move to database."

    # in here create csv table and storage it, make name's can do it and yaml tables have it's information
    for i in range(2, g_all_length):
        value_temp = yl.deal_val_strategy(raw_values[i])

        if value_temp[10] in file_name_vals:
            temp_id = test_db.insert_yaml(table2, message, value_temp)
            print "The insert value's csv_file name: %s " % value_temp[10]  # 0 1 2 3 4 5 6 7 8 9 10
            if value_temp[10] in file_names:
                s = dir_name + '/' + value_temp[10]
                name = value_temp[10][:-4]
                name1 = deal_name(name)
                print name1
                create_table(name1, message)
                storage(name1, s, message)
                storage_name(name1, table, message, temp_id)
    insert_index_names_16(table, message)
    
    

# 需要与之对应的 更新操作者的名字和时间函数， 这里需要对16个指标都进行修改炒作
def insert_index_names(table, message):
    name_two_value = get_name_stoploss_pointvalue(table, message)
    names = get_name(table, message)
    '''
    sql = "insert into %s(NP, MDD, PpT, TT, ShR, Days, " \
          "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    '''

    num = 0

    for name in names:
        t1 = time.time()
        # 需要进行修改调用值
        val = get_index.get_index14(name, message)  # get the index of table name it need a change!
        val0_temp = get_index.get_index16(name, message)
        # val = []
        t3 = time.time()
        print 'single 1 time:\t', (t3 - t1)
        sql = "insert into "+table+"(NP, MDD, PpT, TT, ShR, Days, " \
              "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
              val[0], val[0], val[0], val[0], val[0], \
              val[0], val[0], val[0], val[0], val[0], \
              val[0], val[0], val[0], val[0])

        sql2 = "update " + table + " set NP=%s, MDD=%s, PpT=%s, TT=%s, ShR=%s, Days=%s, D_WR=%s, D_STD=%s, " \
                                   "D_MaxNP=%s, D_MinNP=%s, maxW_Days=%s, maxL_Days=%s, mDD_mC=%s, mDD_iC=%s, " \
                                   "LVRG=%s, LVRG_Mon_NP=%s where name='%s'" % (val[0], val[1], val[2], val[3], val[4],
                                                                                val[5], val[6], val[7], val[8], val[9],
                                                                                val[10], val[11], val[12], val[13],
                                                                                val[10], val[11], name)

        sql1 = "update "+table+" set NP=%s, MDD=%s, PpT=%s, TT=%s, ShR=%s, Days=%s, D_WR=%s, D_STD=%s, D_MaxNP=%s," \
                               " D_MinNP=%s, maxW_Days=%s, maxL_Days=%s, mDD_mC=%s, mDD_iC=%s where name='%s'" % (
              val[0], val[1], val[2], val[3], val[4], \
              val[5], val[6], val[7], val[8], val[9], \
              val[10], val[11], val[12], val[13], name)

        conn = connect_database(message)
        cursor = conn.cursor()
        cursor.execute(sql1)
        conn.commit()
        cursor.close()
        conn.close()
        t2 = time.time()
        print "num: %d\t" % num, (t2 - t1)

        print sql1
        num += 1


# change
# right  :2018/3/24 20:51
def insert_index_names_16(table, message):
    name_two_value = get_name_stoploss_pointvalue(table, message)
    # names = get_name(table, message)
    '''
    sql = "insert into %s(NP, MDD, PpT, TT, ShR, Days, " \
          "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    '''

    num = 0

    for val_3 in name_two_value:
        t1 = time.time()
        # 需要进行修改调用值
        # get the index of table name it need a change!
        val = get_index.get_index16(val_3[0], message, val_3[1], val_3[2])
        # val = []
        t3 = time.time()
        print 'single 1 time:\t', (t3 - t1)
        sql = "insert into "+table+"(NP, MDD, PpT, TT, ShR, Days, " \
              "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (
              val[0], val[0], val[0], val[0], val[0], \
              val[0], val[0], val[0], val[0], val[0], \
              val[0], val[0], val[0], val[0])

        sql2 = "update " + table + " set NP=%s, MDD=%s, PpT=%s, TT=%s, ShR=%s, Days=%s, D_WR=%s, D_STD=%s, " \
                                   "D_MaxNP=%s, D_MinNP=%s, maxW_Days=%s, maxL_Days=%s, mDD_mC=%s, mDD_iC=%s, " \
                                   "LVRG=%s, LVRG_Mon_NP=%s where name1='%s'" % (val[0], val[1], val[2], val[3], val[4],
                                                                                val[5], val[6], val[7], val[8], val[9],
                                                                                val[10], val[11], val[12], val[13],
                                                                                val[14], val[15], val_3[0])

        sql1 = "update "+table+" set NP=%s, MDD=%s, PpT=%s, TT=%s, ShR=%s, Days=%s, D_WR=%s, D_STD=%s, D_MaxNP=%s," \
                               " D_MinNP=%s, maxW_Days=%s, maxL_Days=%s, mDD_mC=%s, mDD_iC=%s where name1='%s'" % (
              val[0], val[1], val[2], val[3], val[4], \
              val[5], val[6], val[7], val[8], val[9], \
              val[10], val[11], val[12], val[13], val_3[0])

        conn = connect_database(message)
        cursor = conn.cursor()
        cursor.execute(sql2)
        conn.commit()
        cursor.close()
        conn.close()
        t2 = time.time()
        print "num: %d\t" % num, (t2 - t1)

        print sql2
        num += 1


# a big csv to database;
# single one
# (-_-) 10s for 27level, two 1:np.load 3 two 2: pd.read_sql 7
def storage(table_name, file_name, message):
    val1, val2, val3, val4, val5, val6, val7, val8 \
        = np.loadtxt(file_name, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True)
    t1 = "insert into %s (a, b, c1, d, e, f, g, h)" % table_name
    print t1
    length = len(val1)
    print length
    number = 45000
    n = length/number

    '''
    if n > 0:
        return
    '''
    if n > 0:
        num = 0
        for j in range(n):
            params = []
            num += number
            conn = connect_database(message)
            # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
            for i in range(j * number, (j+1)*number):

                values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
                params.append(values)
            sql = t1+" values(%s, %s, %s, %s, %s, %s, %s, %s)"
            cursor = conn.cursor()
            cursor.executemany(sql, params)
            conn.commit()
            cursor.close()
            conn.close()

        l2 = len(val1[n*number:])

        params = []
        conn = connect_database(message)
        # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
        for i in range(n*number, len(val1)):
            values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
            params.append(values)
        sql = t1 + " values(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.executemany(sql, params)
        conn.commit()
        cursor.close()
        conn.close()
    else:
        params = []
        conn = connect_database(message)
        # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
        for i in range(len(val1)):
            values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
            params.append(values)
        sql = t1 + " values(%s, %s, %s, %s, %s, %s, %s, %s)"
        cursor = conn.cursor()
        cursor.executemany(sql, params)
        conn.commit()
        cursor.close()
        conn.close()

'''part 2'''


# just for test the storage part
# (!*_*!)
def read_buck(params, table):
    try:
        print len(params)
        t1 = "insert into %s (a, b, c1, d, e, f, g, h)" % table
        sql = t1 + " values(%s, %s, %s, %s, %s, %s, %s, %s)"
        print sql
        conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
        conn.cursor().executemany(sql, params)
        conn.cursor().close()
        conn.close()
    except Exception as e:
        print e


def test_read(table_name, file_name):
    val1, val2, val3, val4, val5, val6, val7, val8 \
        = np.loadtxt(file_name, delimiter=',', usecols=(0, 1, 2, 3, 4, 5, 6, 7), unpack=True)
    length = len(val1)
    print length
    number = 50000
    n = length / number
    print n
    if n > 0:
        num = 0
        for j in range(n):
            params = []
            num += number
            for i in range(len(val1[j * number:(j+1)*number])):
                values = [str(val1[i]), str(val2[i]), str(val3[i]), str(val4[i]), str(val5[i]), str(val6[i]), str(val7[i]), str(val8[i])]
                params.append(values)
            read_buck(params, table_name)

        l2 = len(val1[n * number:])
        # print l2
        # print num
        params = []
        for i in range(len(val1[n * number:])):
            values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
            params.append(values)
        read_buck(params, table_name)

    else:
        params = []
        for i in range(len(val1)):
            values = [val1[i], val2[i], val3[i], val4[i], val5[i], val6[i], val7[i], val8[i]]
            params.append(values)
        read_buck(params, table_name)

'''part 3'''


# 创建基础筛选csv的指标
def create_names_table(name, table_f, message):
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql = "create table %s(name_id int not null AUTO_INCREMENT," \
          "name1 varchar(200) not null," \
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

    # 未修改前版本
    sql1 = "create table %s(name_id int not null AUTO_INCREMENT," \
          "name1 varchar(200) not null," \
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
          "PRIMARY KEY (name_id)," \
          ")" % name

    cursor = conn.cursor()
    cursor.execute(sql)
    conn.commit()
    conn.close()


# build the table that related with names table
# this version is good!
def create_yaml_table(table, message):

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
    conn = connect_database(message)
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit()
    conn.close()


# just create the basic csv table
def create_table(name, message):
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql0 = "if not exists(select * from sys.Tables where name='"+name+"') "
    sql = "CREATE TABLE "+name+"(csv_id int NOT NULL AUTO_INCREMENT,A  int NOT NULL," \
          "B  int NOT NULL," \
          "C1  int NOT NULL," \
          "D  int NOT NULL," \
          "E  int NOT NULL," \
          "F  int NOT NULL," \
          "G  int NOT NULL," \
          "H  int NOT NULL," \
          "PRIMARY KEY ( csv_id )" \
          ")"
    su = sql0 + sql
    # print su
    sql2 = "CREATE TABLE IF NOT EXISTS " + name + \
           "(csv_id int NOT NULL AUTO_INCREMENT," \
           "A  int NOT NULL," \
           "B  int NOT NULL," \
           "C1  float NOT NULL," \
           "D  int NOT NULL," \
           "E  int NOT NULL," \
           "F  float NOT NULL," \
           "G  int NOT NULL," \
           "H  int NOT NULL," \
           "PRIMARY KEY ( csv_id )) "

    sql3 = "CREATE TABLE " + "test-112" + \
           "(csv_id int NOT NULL AUTO_INCREMENT," \
           "A  int NOT NULL," \
           "B  int NOT NULL," \
           "C1  float NOT NULL," \
           "D  int NOT NULL," \
           "E  int NOT NULL," \
           "F  float NOT NULL," \
           "G  int NOT NULL," \
           "H  int NOT NULL," \
           "PRIMARY KEY ( csv_id ))"

    cursor = conn.cursor()
    cursor.execute(sql2)
    conn.close()


def create_index_table():
    pass

'''part 4'''


# using
def insert_index_names1(table):
    names = get_name(table)
    '''
    sql = "insert into %s(NP, MDD, PpT, TT, ShR, Days, " \
          "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
          "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    '''
    print names
    for name in names:
        val = test6.plot_result1(name)  # get the index of table name
        val = []
        sql = "insert into %s(NP, MDD, PpT, TT, ShR, Days, " \
              "D_WR, D_STD, D_MaxNP, D_MinNP, maxW_Days, maxL_Days, mDD_mC, mDD_iC)" \
              "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % (name, val[0], val[0], val[0], val[0], val[0], \
                                                                            val[0], val[0], val[0], val[0], val[0], \
                                                                          val[0], val[0], val[0], val[0])
        print sql


# just test
def insert_values(values, table_name):
    conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql1 = "insert into "+table_name+"(a, b, c1, d, e, f, g, h) values("+str(values[0])+","+str(values[1])+","+str(values[2])+","+str(values[3])+","+str(values[4])+","\
    +str(values[5]) + ","+str(values[6])+","+str(values[7])+")"
    cursor = conn.cursor()
    cursor.execute(sql1)
    conn.commit()
    conn.close()

'''part 5'''


# just for test get the value from mysql  (!-_-!)
def get_values(table_name, message):
    conn = connect_database(message)
    # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
    sql2 = 'select a, b, c1, d, e, f, g, h from '+table_name
    cursor = conn.cursor()
    cursor.execute(sql2)
    values = cursor.fetchall()
    val1 = []
    val2 = []
    val3 = []
    val4 = []
    val5 = []
    val6 = []
    val7 = []
    val8 = []

    # print values
    for row in values:
        val1.append(row[0])
        val2.append(row[1])
        val3.append(row[2])
        val4.append(row[3])
        val5.append(row[4])
        val6.append(row[5])
        val7.append(row[6])
        val8.append(row[7])
    conn.close()
    # print val1

'''part 6'''


# delete the pack tables in a name table
def delete_csv_table(table, message):
    names = get_name(table, message)
    le = len(names)
    print le
    if le > 0:
        print names
        for i in range(le):
            database = connect_database(message)
            delete_table(names[i], database)
        database = connect_database(message)
        delete_value('names', database)
    else:
        print "Empty!"


def delete_value(table, database):
    try:
        conn = connect_database(database)
        sql = 'TRUNCATE TABLE ' + table
        print sql
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print "TRUNCATE TABLE: %s\t" % table, e


def delete_table(table_name, database):
    try:
        # conn = mdb.connect(host='127.0.0.1', user='root', passwd='7ondr', db='test')
        conn = database
        sql = 'drop table ' + table_name
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        conn.close()
    except Exception as e:
        print "drop table: %s\t" % table_name, e


message = ['127.0.0.1', 'root', '7ondr', 'testpy']
table1 = 'all_species_table_test1'
# create_table('show_me', message)
# create_names_table('test_name_new', 'yaml_table_test', message)
# storage('show_me', 'test.csv', message)
# csv_to_database(message)
# delete_value('all_species_table_test1', message)
# insert_index_names('names', message)
# delete_csv_table('test_name_new', message)
# create_yaml_table('yaml_table_test', message)  # 针对每一个品种都需要一个yaml——table 和一个 name table1

get_raw_data(table_all=table1, dir_name='test1', table='test_name_new', table2='yaml_table_test', message=message)
# insert_index_names_16('test_name_new', message)


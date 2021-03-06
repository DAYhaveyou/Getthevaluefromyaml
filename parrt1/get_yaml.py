import yaml
import time
import test_db



def get_raw_data(file_name, table, message):
    print "Please wait to get the yaml data! name:\t %s" % file_name
    g_t1 = time.time()
    f_value = open(file_name)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    raw_values = raw_values
    g_all_length = len(raw_values)
    # print g_all_length
    print "Now read the data to move to database."
    for i in range(g_all_length):
        value_temp = deal_val_strategy(raw_values[i])
        temp_id = test_db.insert_yaml(table, message, value_temp)
        print "The insert value's csv_file name: %s " % value_temp[10]  # 0 1 2 3 4 5 6 7 8 9 10


def deal_val_strategy(value):
    # part 1: used for the strategy information
    strategy = value[0]['Strategy']  # string

    # part 2: the information of strategy
    Config_WarmUp = value[1]['Config']['WarmUp']  # float
    Config_KBarPeriod_KBarTimeMin = value[1]['Config']['KBarPeriod']['KBarTimeMin']  # int
    Config_Parameters = value[1]['Config']['Parameters']  # string

    # part 3: the optimum
    optimum_num = value[2]['Optimum'][0]  # int
    optimum_total_time = value[2]['Optimum'][1]  # string
    optimum_values = value[2]['Optimum']
    # part 3+1: need another type table to storage
    '''
    Optimum_length = len(value[2]['Optimum'])
    for Optimum_num in range(2, Optimum_length):
        Optimum_name = value[2]['Optimum'][0]
        Optimum_value = value[2]['Optimum']
    '''
    # part 4:back_test
    back_test_num = value[3]['backtest'][0]
    back_test_period = value[3]['backtest'][1]
    back_test_value = value[3]['backtest']

    # part 4: name
    csv_name = value[4]['bkt.csv'][0]

    return strategy, Config_WarmUp, Config_KBarPeriod_KBarTimeMin, Config_Parameters, optimum_num, optimum_total_time, \
            optimum_values, back_test_num, back_test_period, back_test_value, csv_name


# This just used for 5 levels, if the level is N. please make huff man tree
def deal_data5_of_unknown(raw_value):  # ready for back_test
    raw_data = []  # 1
    raw1_data = []  # 2
    raw2_data = []  # 3
    raw3_data = []  # 4
    raw4_data = []  # 5
    count_type = 0  # max is 5
    str = ""
    str_flag = 1
    for c in raw_value:
        if c == '[':
            count_type += 1
        elif c == ']':
            # str = ""
            if count_type == 1:
                if str_flag == 1:
                    if str.find('.') != -1:
                        raw_data.append(float(str))
                    elif str.isdigit():
                        raw_data.append(int(str))
                    else:
                        raw_data.append(str)  # give 'inf'
                break  # the value is over!
            elif count_type == 2:
                if str_flag != 0:
                    if str.find('.') != -1:
                        raw1_data.append(float(str))
                    elif str.isdigit():
                        raw1_data.append(int(str))
                    else:
                        raw1_data.append(str)
                    # raw1_data.append(float(str))
                    str = ""
                raw_data.append(raw1_data)
                raw1_data = []
            elif count_type == 3:
                if str_flag != 0:
                    if str.find('.') != -1:
                        raw2_data.append(float(str))
                    elif str.isdigit():
                        raw2_data.append(int(str))
                    else:
                        raw2_data.append(str)
                    # raw1_data.append(float(str))
                    str = ""
                raw1_data.append(raw2_data)
                raw2_data = []
            elif count_type == 4:
                if str_flag != 0:
                    if str.find('.') != -1:
                        raw3_data.append(float(str))
                    elif str.isdigit():
                        raw3_data.append(int(str))
                    else:
                        raw3_data.append(str)
                    # raw1_data.append(float(str))
                    str = ""
                raw2_data.append(raw3_data)
                raw3_data = []
            elif count_type == 5:
                if str.find('.') != -1:
                    raw4_data.append(float(str))
                elif str.isdigit():
                    raw4_data.append(int(str))
                else:
                    raw4_data.append(str)
                # raw2_data.append(float(str))
                str = ""
                raw3_data.append(raw4_data)  # if it is the final type then append and over!
                raw4_data = []
            count_type -= 1
            str_flag = 0
        elif c == ',' and str_flag == 1:

            if count_type == 1:
                if str.find('.') != -1:
                    raw_data.append(float(str))
                elif str.isdigit():
                    raw_data.append(int(str))
                else:
                    raw_data.append(str)  # give 'inf'
                # value = float(str)
                # raw_data.append(value)
            elif count_type == 2:
                if str.find('.') != -1:
                    raw1_data.append(float(str))
                elif str.isdigit():
                    raw1_data.append(int(str))
                else:
                    raw1_data.append(str)  # give 'inf'
                # value = float(str)
                # raw1_data.append(value)
            elif count_type == 3:
                if str.find('.') != -1:
                    raw2_data.append(float(str))
                elif str.isdigit():
                    raw2_data.append(int(str))
                else:
                    raw2_data.append(str)  # give 'inf'
                # value = float(str)
                # raw2_data.append(value)
            elif count_type == 4:
                if str.find('.') != -1:
                    raw3_data.append(float(str))
                elif str.isdigit():
                    raw3_data.append(int(str))
                else:
                    raw3_data.append(str)  # give 'inf'
            elif count_type == 5:
                if str.find('.') != -1:
                    raw4_data.append(float(str))
                elif str.isdigit():
                    raw4_data.append(int(str))
                else:
                    raw4_data.append(str)  # give 'inf'
            str = ""
            # continue
        elif c == ' ' or c == "'":
            continue
        elif c != ',':
            str += c
            str_flag = 1

    return raw_data


# This just used for 3 levels
def deal_data3_of_unknown(raw_value):  # ready for back_test
    raw_data = []  # 1
    raw1_data = []  # 2
    raw2_data = []  # 3
    count_type = 0
    str = ""
    str_flag = 1
    for c in raw_value:
        if c == '[':
            count_type += 1
        elif c == ']':
            # str = ""
            if count_type == 1:
                if str_flag == 1:
                    if str.find('.') != -1:
                        raw_data.append(float(str))
                    else:
                        raw_data.append(int(str))
                break  # the value is over!
            elif count_type == 2:
                if str_flag != 0:
                    if str.find('.') != -1:
                        raw1_data.append(float(str))
                    else:
                        raw1_data.append(int(str))
                    # raw1_data.append(float(str))
                    str = ""
                raw_data.append(raw1_data)
                raw1_data = []
            elif count_type == 3:
                if str.find('.') != -1:
                    raw2_data.append(float(str))
                else:
                    raw2_data.append(int(str))
                # raw2_data.append(float(str))
                str = ""
                raw1_data.append(raw2_data)  # if it is the final type then append and over!
                raw2_data = []
            count_type -= 1
            str_flag = 0
        elif c == ',' and str_flag == 1:

            if count_type == 1:
                if str.find('.') != -1:
                    raw_data.append(float(str))
                else:
                    raw_data.append(int(str))
                # value = float(str)
                # raw_data.append(value)
            elif count_type == 2:
                if str.find('.') != -1:
                    raw1_data.append(float(str))
                else:
                    raw1_data.append(int(str))
                # value = float(str)
                # raw1_data.append(value)
            elif count_type == 3:
                if str.find('.') != -1:
                    raw2_data.append(float(str))
                else:
                    raw2_data.append(int(str))
                # value = float(str)
                # raw2_data.append(value)
            str = ""
            # continue
        elif c == ' ':
            continue
        elif c != ',':
            str += c
            str_flag = 1
        '''
        if count_type == 1:
            value = float(str)
            raw_data.append(value)
        elif count_type == 2:
            value = float(str)
            raw1_data.append(value)
        elif count_type == 3:
            value = float(str)
            raw2_data.append(value)
        '''
    return raw_data


def deal_data_of_optimum(raw_value):
    pass

# s3 = deal_data_of_unknown(s31)
# for i in range(3):
#     print s3[i]

message1 = ['127.0.0.1', 'root', '7ondr', 'test']
table1 = 'yaml_table'
# get_raw_data('T4.yaml', table, message)


def test_unit(table, message):
    a1 = test_db.get_value_yaml(table, message)
    a2 = deal_data5_of_unknown(a1)
    print a1
    print a2
    print type(a1), type(a2)
    if a1 == str(a2):
        print "Your function is not bad!"

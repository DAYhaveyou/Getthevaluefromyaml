def test_unit(table, message):
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
    print "Please wait to get the yaml data! name:\t %s" % yaml_file
    g_t1 = time.time()
    f_value = open(yaml_file)
    raw_values = yaml.load(f_value)
    g_t2 = time.time()
    print "Load yaml over! Cost time: %.3f" % (g_t2 - g_t1)
    g_all_length = len(raw_values)
    for i in range(2, g_all_length):
        g_t3 = time.time()
        # value_temp = yl.deal_val_strategy(raw_values[i])
        value_temp = yl.deal_val_strategy(raw_values[i])
        temp_id = test_db.insert_yaml(table, message, value_temp)
        g_t4 = time.time()
        # print "Num %d cost %f s" % (temp_id, (g_t4 - g_t3))
        print "Num ", temp_id, " cost ", (g_t4 - g_t3), "s"
        if value_temp[10] in file_names:
            file_num += 1
    print "The total file number: ", file_num

import DB_Connect,db_oprate



def copy_sql_mongo(data):
    tmp_dict = {}
    tmp_dict['RID'] = data[0]
    tmp_dict['QID'] = data[1]
    tmp_dict['Article_Title'] = data[2]
    tmp_dict['Article_Descr'] = data[3]
    tmp_dict['Article_Keywords'] = data[4]
    tmp_dict['Article_Domain'] = data[5]
    tmp_dict['Article_GroupID'] = data[6]
    tmp_dict['Article_CateID'] = data[7]
    tmp_dict['Article_fromURL'] = data[8]
    tmp_dict['Article_Path'] = data[9]
    tmp_dict['Article_Tags'] = data[10]
    tmp_dict['Article_Lenth'] = data[11]
    tmp_dict['Article_Content'] = data[12]
    tmp_dict['isCompare'] = data[13]
    tmp_dict['isUsed'] = data[14]
    tmp_dict['IsNote'] = data[15]
    tmp_dict['Article_Note'] = data[16]
    tmp_dict['isUse'] = data[17]
    tmp_dict['KWS'] = data[18]
    tmp_dict['isFind'] = data[19]
    return tmp_dict


obj = db_oprate.collection_db()
obj1 = DB_Connect.task_opt()

while True:
    data_col = obj1.select_Article_List()
    for item in data_col:
        try:
            tmp = copy_sql_mongo(item)
            obj.insert_data(obj.tb,tmp)
            obj1.update_Article_flag(item[0])
        except Exception as e:
            print(e)
            print ('出错')


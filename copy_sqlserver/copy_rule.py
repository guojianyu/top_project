import DB_Connect1,db_oprate


def copy_sql_mongo(data):
    tmp_dict = {}
    tmp_dict['RID'] = data[0]
    tmp_dict['Task_Name'] = data[1]
    tmp_dict['Task_URL'] = data[2]
    tmp_dict['Task_On_rule'] = data[3]
    tmp_dict['Task_Out_rule'] = data[4]
    tmp_dict['Task_Deep'] = data[5]
    tmp_dict['Task_Status'] = data[6]
    tmp_dict['Task_isClear'] = data[7]
    tmp_dict['Task_isReset'] = data[8]
    tmp_dict['Task_Match_field'] = data[9]
    tmp_dict['Task_Match_rule'] = data[10]
    tmp_dict['Creat_Date'] = data[11]
    tmp_dict['Task_Level'] = data[12]
    return tmp_dict


obj = db_oprate.collection_db()
obj1 = DB_Connect1.task_opt()

"""
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
"""
if __name__ == "__main__":
    data_col = obj1.test()
    for item in data_col:
        tmp = copy_sql_mongo(item)
        obj.insert_data(tmp)
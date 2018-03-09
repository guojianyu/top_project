import DB_Connect
db_obj = DB_Connect.task_opt()# 操作数据库对象

def group_cipin():
    a = db_obj.look1()
    with open('auto_clean_data.txt','w') as f:
        f.write(str(a))
def look_group_all(cipin_3):
    a = db_obj.look(cipin_3)
    for item in a:
        print (item)

a = look_group_all('病人|肛门|痔疮')
print (a)

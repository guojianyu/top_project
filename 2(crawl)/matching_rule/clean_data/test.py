import re
import DB_Operation
""""
截取
ab|‘’
‘’|ab
从ab截取到最后，从开始截取到ab

替换：
ab|''
ab|ba


"""

db_boj= DB_Operation.collection_db()
#db_boj.insert_data({'split': "真|",'replace':"你好|我好","Task_RID":30,"Task_Status":0})
dict = db_boj.select_clear_task()
if not dict:
    pass

#dict = {'split': "真|",'replace':"你好|我好","Task_RID":30,"Task_Status":0}
#Task_Status 任务执行状态
#Task_IsComplete 任务是否完成
split =dict['split']
replace = dict['replace']
print (split,type(split))
if split:
    html = "你好吗真饿大 真你好是的发饿发该呆湾我发该饿是烦你好你好烦烦事实上我 淡淡的你不你不"
    re_math = '(?i)%s(.*)%s' % (split[0], split[1])
    print(re_math)
    result = re.findall(re_math, html, re.DOTALL)  # 匹配所有
    if not result:  # 没有匹配到结果
        result = html
    else:
        result = result[0]
    print(result)
else:
    pass
if replace:
    result = result.replace(replace[0], replace[1])
    print (result)






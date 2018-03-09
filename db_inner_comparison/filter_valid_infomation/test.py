import DB_Connect
import db_oprate
import jieba.analyse
import xlrd

workbook = xlrd.open_workbook(r'C:\untitled\db_inner_comparison\similar_comparison\匹配词.xlsx')
sheet1 = workbook.sheet_by_name('Sheet1')
col_content = sheet1.col_values(0)
match_sum = 0#统计匹配总数
word_count = {}#统计每个词的出现次数
data_sum=0
def cut_word(article):
    # 这里使用了TF-IDF算法，所以分词结果会有些不同->https://github.com/fxsjy/jieba#3-关键词提取
    res = jieba.analyse.extract_tags(
        sentence=article,allowPOS=( 'n','1','ns','v'))
    return res
def sql_read_data(ci=''):
    global data_sum
    t = DB_Connect.task_opt()
    a = t.look1()
    filter_valid_info(a)

def filter_valid_info(data_list):#过滤有效信息
    for item in data_list:
        print('标题:', item[1])
        ci = cut_word(item[1])
        print('词频：', ci)
        if not ci:
            continue
        record_word_excel(ci,item[1])
    pass
def record_word_excel(words_list,title):
    find_flag =0
    global match_sum
    global word_count
    for word in words_list:
        if word in col_content:
            find_flag =1
            match_sum +=1
            try:
                word_count[word] +=1
            except:
                word_count[word]=1
            break
    if not find_flag:
        print ('没有匹配到的标题为：',title)
    else:
        print ('匹配到的标题为：',title)

if __name__ == '__main__':
    #[(1,'肠癌吃什么药物好吗'),]
    #sql_read_data()
    #read_excel(['肠病','芦荟'])
    # obj.insert_data(obj.tb,{'a':1,'b':2(crawl)})
    #mongo_read_data()
    #filter_valid_info()
    sql_read_data()

    #record_word_excel()
   # print ('总计匹配个数为：',match_sum)
   # print ('词频与个数统计结果:',word_count)
    #print ('匹配率为：',match_sum/data_sum)
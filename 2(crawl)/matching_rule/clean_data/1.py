import re
def system_default_clean(content):  # 系统默认替换的信息字符串
    clean_date_match = '\d{0,4}[-/年]\d{0,2}[-/月]\d{0,2}[日]{0,1}'  # 数字时间去除
    clean_time_match = "\d{0,2}[:/时]\d{0,2}[:/分]\d{0,2}[秒]{0,1}"
    result = ''# 替换成的结果
    content = re.sub(clean_date_match, result, content)
    content = re.sub(clean_time_match, result, content)
    content = content.strip()  # 去掉开头结尾空白符
    content = content.replace(" ",'')
    return content

a = "你好2017-2-2        11:20:20aaa        a"
#a = "是吗2017-2-2达到 "
b = system_default_clean(a)
print (b)
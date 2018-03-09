import math
import jieba.analyse
def cut_word(article):
    # 这里使用了TF-IDF算法
    res = jieba.analyse.extract_tags(
        sentence=article, topK=20, withWeight=True,allowPOS=('n',))
    return res

def tf_idf(res1=None, res2=None):
    # 向量，可以使用list表示
    vector_1 = []
    vector_2 = []
    # 词频，可以使用dict表示
    tf_1 = {i[0]: i[1] for i in res1}
    tf_2 = {i[0]: i[1] for i in res2}
    res = set(list(tf_1.keys()) + list(tf_2.keys()))
    # 填充词频向量
    for word in res:
        if word in tf_1:
            vector_1.append(tf_1[word])
            if word in tf_2:
                vector_2.append(tf_2[word])
            else:
                vector_2.append(0)
        else:
            vector_1.append(0)
            if word in tf_2:
                vector_2.append(tf_2[word])

    return vector_1, vector_2


def numerator(vector1, vector2):
    #分子
    return sum(a * b for a, b in zip(vector1, vector2))

def denominator(vector):
    #分母
    return math.sqrt(sum(a * b for a,b in zip(vector, vector)))


def run(vector1, vector2):
    try:
        res = numerator(vector1,vector2) / (denominator(vector1) * denominator(vector2))
    except:
        res = 0
    return res

def similarity(text1,text2):
    res1 = cut_word(text1)
    res2 = cut_word(text2)
    print (res1)
    print (res2)
    vectors = tf_idf(res1=res1, res2=res2)
    similar = run(vector1=vectors[0], vector2=vectors[1])
    return similar
if __name__ =='__main__':
    text1 ='网易有道以搜索产品和技术为起点，在大规模数据存储计算等领域具有深厚的技术积累，并在此基础上衍生出语言翻译应用与服务、个人云应用和电子商务导购服务等三个核心业务方向。'
    text2 = '中国爱我'
    a = similarity(text1,text2)
    print (type(a))
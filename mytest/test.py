import jieba
import jieba.posseg as psg
txt = '肺癌饮食吃菠菜比较好？'
"""
jieba.load_userdict('C:\\untitled\\mytest\\jayguo.txt')
seg_list = jieba.cut(txt)
print("Revise: " + "/".join(seg_list))
"""
#print ([(x.word,x.flag) for x in psg.cut(txt)])

print ([(x.word,x.flag) for x in psg.cut(txt) if x.flag.startswith('n')])
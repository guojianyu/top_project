import csv
filename = input("请输入文件名")

a = input("请输入添加文字")
csvFile = open(filename+".csv", "r")
reader = csv.reader(csvFile)
tmp = []
for item in reader:
    c = item[0]+a
    item.append(c)
    tmp.append(item)

csvFile = open("鼻咽.csv", "w")
writer = csv.writer(csvFile)
for i in tmp:
    writer.writerow(i)
csvFile.close()
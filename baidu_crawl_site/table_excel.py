import xlwt
import  DB_Connect
excel = xlwt.Workbook(encoding='utf-8')
worksheet = excel.add_sheet('My_Worksheet.xls')

site_coll = [[1,2,3],[2,3,4],[3,4,5]]
item =1
for data in site_coll:
    print (item)
    worksheet.write(item, 0, data[0])
    worksheet.write(item, 1, data[1])
    worksheet.write(item, 2, data[2])
    item +=1

excel.save('My_Worksheet.xls')
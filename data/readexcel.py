# _*_ coding:utf-8 _*_
import pandas as pd  #先装个pandas ,pip install pandas
import pymysql

#读入数据库
filename = '2011-2021年上海各区房价月度数据.xlsx'  #本地需要导入数据库的文件
data = pd.read_excel(filename)
#建立数据库连接
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='sxy000217',
                     database='house_project')
cursor = db.cursor()

query = 'insert into departmentprice(UniqueCode,District,Price,PriceTime,SourceId) values (%s,%s,%s,%s,%s)'
num = 1
for row_index, row in data.iterrows():
    for col in range(data.shape[1]):
        UniqueCode = num
        SourceId = 1
        PriceTime = row[0].strftime("%Y-%m-%d")

        if col >= 1:
            Price = row[col]
            District = data.columns[col]
            values = (UniqueCode, str(District), int(Price), str(PriceTime),
                      SourceId)
            cursor.execute(query, values)
            num = num + 1

cursor.close()
db.commit()
print("数据导入成功")
db.close()
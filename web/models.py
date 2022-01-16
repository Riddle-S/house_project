from django.db import models
from datetime import datetime


# Create your models here.
#二手房房价数据模型
class Departmentprice(models.Model):
    UniqueCode = models.CharField(max_length=10, primary_key=True)  #数据标识码
    District = models.CharField(max_length=30)  #地区
    Price = models.IntegerField()  #价格
    PriceTime = models.CharField(max_length=30)  #价格时间
    SourceId = models.CharField(max_length=10)  #数据来源,1代表网络搜寻得到,具体id代表用户id

    def toDict(self):
        return {
            'UniqueCode': self.UniqueCode,
            'District': self.District,
            'Price': self.Price,
            'PriceTime': self.PriceTime.strftime('%Y-%m-%d '),
            'SourceId': self.SourceId,
        }

    class Meta:
        db_table = "departmentprice"  # 更改表名


#待确认房价信息模型
class Verifypricemessage(models.Model):
    UniqueID = models.CharField(max_length=10, primary_key=True)  #信息编号1,2,3
    District = models.CharField(max_length=30)  #地区
    Price = models.IntegerField()  #价格
    PriceTime = models.CharField(max_length=30)  #价格时间
    SourceId = models.CharField(max_length=10)  #数据来源,1代表网络搜寻得到,具体id代表用户id
    State = models.IntegerField()  #目前状态,0:待确认,1:已确认
    SubmitTime = models.CharField(max_length=30)  #提交时间

    def toDict(self):
        return {
            'UniqueCode': self.UniqueCode,
            'District': self.District,
            'Price': self.Price,
            'PriceTime': self.PriceTime.strftime('%Y-%m-%d '),
            'SourceId': self.SourceId,
            'State': self.State,
            'SubmitTime': self.SubmitTime.strftime('%Y-%m-%d '),
        }

    class Meta:
        db_table = "verifypricemessage"  # 更改表名
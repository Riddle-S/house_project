from django.db import models
from datetime import datetime


#用户账号信息模型
class User(models.Model):
    UserID = models.CharField(max_length=10, primary_key=True)  #用户账号
    Username = models.CharField(max_length=10)  #昵称
    District = models.CharField(max_length=30)  #地区
    Passwordhash = models.CharField(max_length=100)  #密码
    Passwordsalt = models.CharField(max_length=30)  #密码干扰值
    AdminState = models.IntegerField(default=0)  #状态:1管理员,0普通用户,2超管
    Sex = models.IntegerField()  #性别
    Telephone = models.CharField(max_length=30)  #密码干扰值
    Age = models.IntegerField()  #年龄

    def toDict(self):
        return {
            'UserID': self.UserID,
            'Username': self.Username,
            'District': self.District,
            'Passwordhash': self.Passwordhash,
            'Passwordsalt': self.Passwordsalt,
            'AdminState': self.AdminState,
            'Sex ': self.Sex,
            'Telephone': self.Telephone,
            'Age': self.Age,
        }

    class Meta:
        db_table = "user"  # 更改表名

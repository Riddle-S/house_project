#后台管理子路由文件
from django.urls import path
from myadmin.views import index  #myadmin的views包中的Index文件
from myadmin.views import user, price

urlpatterns = [
    path('', index.index, name='myadmin_index'),  #index文件中的index函数
    #后台管理员登陆、退出路由
    path('login', index.login, name='myadmin_login'),  #加载登录表单
    path('dologin', index.dologin, name="myadmin_dologin"),  #执行登录
    path('logout', index.logout, name="myadmin_logout"),  #退出
    path('verify', index.verify, name="myadmin_verify"),  #输出验证码
    #用户注册
    path('register', index.register, name='myadmin_register'),  #加载注册表单
    path('doregister', index.doregister, name='myadmin_doregister'),  #执行注册
    #用户信息管理路由
    path('user/<int:pindex>', user.index, name='myadmin_user_index'),  #浏览
    path('user/add', user.add, name='myadmin_user_add'),  #添加表单
    path('user/insert', user.insert, name='myadmin_user_insert'),  #执行添加
    path('user/del/<int:uid>', user.delete, name='myadmin_user_delete'),  #执行删除
    path('user/edit/<int:uid>', user.edit, name='myadmin_user_edit'),  #加载编辑表单
    path('user/update/<int:uid>', user.update,
         name='myadmin_user_update'),  #执行编辑
    path('user/profile/<int:uid>', user.profile,
         name='myadmin_user_profile'),  #执行编辑
    path('user/userupdate/<int:uid>',
         user.userupdate,
         name='myadmin_user_userupdate'),
    #房价信息查看
    path('price/<int:pindex>', price.index, name='myadmin_price_index'),  #浏览
]

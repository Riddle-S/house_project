from django.shortcuts import redirect
from django.urls import reverse

import re


class Middleware:
    '''自定义中间件类(执行是否登录判断)'''
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.一次性调用

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.每次都会被调用
        path = request.path
        print("url:", path)

        #判断管理后台是否登录
        #定义后台不登陆也可以直接访问的url列表
        urllist = [
            '/myadmin/login',  #注意要带斜杠
            '/myadmin/logout',
            '/myadmin/dologin',
            '/myadmin/verify',
            '/myadmin/register',
            '/myadmin/doregister'
        ]
        #判断当前请求url地址是否以/myadmin开头(后台),并且不在允许的urllist中,才做是否登陆判断
        if re.match(r'^/myadmin', path) and (path not in urllist):
            #重定向到登录页(在session中没有adminuser,session是字典格式)
            if 'adminuser' not in request.session:
                return redirect(reverse("myadmin_login"))
        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
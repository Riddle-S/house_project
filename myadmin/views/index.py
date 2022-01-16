from django.shortcuts import render, redirect
from django.http import HttpResponse
from myadmin.models import User
from django.urls import reverse
from data import support

# Create your views here.


#后台管理首页
def index(request):
    return render(request, 'myadmin/index/index.html')  #管理员后台


#管理员登录表单
def login(request):
    return render(request, 'myadmin/index/login.html')


#执行用户登陆
def dologin(request):  #记得保存mysql的修改！！！
    try:
        #根据登陆账号获取登陆者信息
        name = request.POST['Username']
        user = User.objects.get(Username=name)
        #判断登录密码是否相同
        import hashlib
        md5 = hashlib.md5()
        s = request.POST['password'] + user.Passwordsalt  #取明文密码并加盐
        md5.update(s.encode('utf-8'))  #将要产生md5的子串放进去
        if user.Passwordhash == md5.hexdigest():  #获取md5值
            #执行验证码的校验
            if request.POST['code'] == request.session[
                    'verifycode']:  #前者表单提交,后者session存取
                #将当前登陆成功的用户信息以adminuser为key写入到session中
                request.session["adminuser"] = user.toDict(
                )  #model类中将User对象转成字典格式的函数
                #重定向到后台管理首页
                if user.AdminState <= 2:
                    return redirect(reverse("myadmin_index"))
                else:
                    context = {"info": "无效的登陆账号"}
            else:
                context = {"info": "验证码错误！"}
        else:
            context = {"info": "登陆密码错误！"}

    except Exception as err:
        print(err)
        context = {"info": "登陆账号不存在"}
    return render(request, "myadmin/index/login.html", context)


#管理员注册表单
def register(request):
    return render(request, 'myadmin/index/register.html')


#执行注册
def doregister(request):  #记得保存mysql的修改！！！
    try:
        #根据登陆账号获取登陆者信息
        name = request.POST['Username']
        password = request.POST['password']
        repassword = request.POST['repassword']
        print(name, password, repassword, request.POST['district'])
        if User.objects.filter(Username=name).count():
            # object.get()得到的是一个对象，如果在数据库中查不到这个对象或者查找到对象都会报错！！！
            # object.filter() 返回的是一个对象列表。如果在数据库中找不到这个对象，那么会返回一个空列表[]
            context = {"info": "该用户名已存在！请尝试其他用户名"}
        else:
            checkresult = support.check_password(password)
            print("here")
            if checkresult == 1:
                context = {"info": "密码应至少为8位！"}
            elif checkresult == 2:
                context = {"info": "密码应至少含有1位数字！"}
            elif checkresult == 3:
                context = {"info": "密码应至少含有1位字母！"}
            else:
                if password != repassword:
                    context = {"info": "两次输入的密码不同！"}
                else:
                    if request.POST['code'] == request.session['verifycode']:
                        import hashlib, random
                        md5 = hashlib.md5()
                        newpasswordsalt = support.create_salt()
                        s = request.POST[
                            'password'] + newpasswordsalt  #取明文密码并加盐
                        md5.update(s.encode('utf-8'))  #将要产生md5的子串放进去
                        newpasswordhash = md5.hexdigest()  #存储hash密码
                        '''执行信息添加'''
                        ob = User()
                        ob.UserID = support.create_id()
                        ob.Username = name
                        ob.Passwordhash = newpasswordhash
                        ob.Passwordsalt = newpasswordsalt
                        ob.District = request.POST['district']
                        ob.AdminState = 0
                        ob.save()
                        context = {"info": "注册成功！"}
                        #重定向到后台管理首页
                        return render(request, "myadmin/index/login.html",
                                      context)
                    else:
                        context = {"info": "验证码错误！"}
    except Exception as err:
        context = {"info": "发生了意外错误！"}
    return render(request, "myadmin/index/register.html", context)


#管理员退出
def logout(request):
    del request.session['adminuser']
    return redirect(reverse('web_index'))


#输出验证码
def verify(request):
    #引入随机函数模块
    import random
    from PIL import Image, ImageDraw, ImageFont
    #定义变量，用于画面的背景色、宽、高
    #bgcolor = (random.randrange(20, 100), random.randrange(
    #    20, 100),100)
    bgcolor = (242, 164, 247)
    width = 100
    height = 25
    #创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    #创建画笔对象
    draw = ImageDraw.Draw(im)
    #调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    #定义验证码的备选值
    str1 = '0123456789'
    #随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    #构造字体对象，ubuntu的字体路径为“/usr/share/fonts/truetype/freefont”
    font = ImageFont.truetype('static/fonts/msyh.ttc', 21)
    #font = ImageFont.load_default().font
    #构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    #绘制4个字
    draw.text((5, -3), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, -3), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, -3), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, -3), rand_str[3], font=font, fill=fontcolor)
    #释放画笔
    del draw
    #存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    """
    python2的为
    # 内存文件操作
    import cStringIO
    buf = cStringIO.StringIO()
    """
    # 内存文件操作-->此方法为python3的
    import io
    buf = io.BytesIO()
    #将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    #将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')
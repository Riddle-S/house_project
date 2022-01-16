#用户信息管理的视图文件
from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q  #或查询
from datetime import datetime
from data import support
# Create your views here.


def index(request, pindex=1):
    '''浏览信息'''
    umod = User.objects.all()  #获取实例对象
    mywhere = []  #状态维持条件
    #获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    ulist = umod.filter()
    if kw:
        ulist = umod.filter(Username__contains=kw)
        mywhere.append('keyword=' + kw)

    #执行分页处理
    pindex = int(pindex)
    upage = Paginator(ulist, 5)  #以每页五条数据分页
    maxpages = upage.num_pages  #获取最大页数
    #获取当前页是否越界
    if pindex > maxpages:
        pindex = maxpages
    if pindex < 1:
        pindex = 1
    list2 = upage.page(pindex)  #获取当前页数据
    plist = [pindex]
    for i in range(1, 6):
        if pindex - i >= 1:
            plist.append(pindex - i)
        if pindex + i <= maxpages:
            plist.append(pindex + i)
    plist.sort()
    context = {
        "userlist": list2,
        'plist': plist,
        'pindex': pindex,
        'maxpages': maxpages,
        'mywhere': mywhere
    }
    return render(request, "myadmin/user/index.html", context)


def add(request):
    '''加载信息添加表单'''
    return render(request, "myadmin/user/add.html")


def insert(request):
    '''执行信息添加'''
    try:
        ob = User()
        ob.Username = request.POST['Username']
        #将当前用户信息的密码做md5处理
        import hashlib, random
        md5 = hashlib.md5()
        n = random.randint(100000, 999999)
        s = request.POST['password'] + str(n)  #从表单中获取密码并添加干扰项
        md5.update(s.encode('utf-8'))  #将要产生md5的子串放进去
        ob.Passwordhash = md5.hexdigest()  #获取md5值
        ob.Passwordsalt = n
        ob.create_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ob.update_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S")  #字符串格式化注意大小写！

        ob.AdminState = 1

        ob.save()
        context = {"info": "添加成功！"}
    except Exception as err:
        print(err)
        context = {"info": "添加失败!"}
    return render(request, "myadmin/info.html", context)


def delete(request, uid=0):
    '''执行信息删除'''
    try:
        ob = User.objects.get(UserID=uid)
        ob.delete()
        context = {"info": "删除成功！"}
    except Exception as err:
        print(err)
        context = {"info": "删除失败!"}
    return render(request, "myadmin/info.html", context)


def edit(request, uid=0):
    '''加载信息编辑表单'''
    try:
        ob = User.objects.get(UserID=uid)
        print(uid)
        context = {'user': ob}
        return render(request, "myadmin/user/edit.html", context)

    except Exception as err:
        print(err)
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def profile(request, uid=0):
    '''加载用户信息页面'''
    try:
        ob = User.objects.get(UserID=uid)
        print(uid)
        context = {'user': ob}
        return render(request, "myadmin/user/profile.html", context)

    except Exception as err:
        print(err)
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "myadmin/info.html", context)


def userupdate(request, uid=0):
    try:
        ob = User.objects.get(UserID=uid)
        ob.Username = request.POST['Username']
        ob.District = request.POST['district']
        if request.POST['password'] != '':
            password = request.POST['password']
            checkresult = support.check_password(password)
            print("here")
            if checkresult == 1:
                context = {"info": "密码应至少为8位！"}
            elif checkresult == 2:
                context = {"info": "密码应至少含有1位数字！"}
            elif checkresult == 3:
                context = {"info": "密码应至少含有1位字母！"}
            else:
                if request.POST['password'] == request.POST['repassword']:
                    import hashlib, random
                    md5 = hashlib.md5()
                    passwordsalt = ob.Passwordsalt
                    s = request.POST['password'] + passwordsalt  #取明文密码并加盐
                    md5.update(s.encode('utf-8'))  #将要产生md5的子串放进去
                    newpasswordhash = md5.hexdigest()  #存储hash密码
                    ob.Passwordhash = newpasswordhash
                    context = {"info": "修改成功！"}
                    request.session["adminuser"] = ob.toDict(
                    )  #model类中将User对象转成字典格式的函数
                    ob.save()
                else:
                    context = {"info": "两次输入密码不同"}
                    return render(request, "myadmin/info.html", context)
            '''执行信息添加'''
        else:
            request.session["adminuser"] = ob.toDict(
            )  #model类中将User对象转成字典格式的函数
            ob.save()
            context = {"info": "修改成功！"}

    except Exception as err:
        print(err)
        context = {"info": "修改失败!"}
    return render(request, "myadmin/info.html", context)


def update(request, uid=0):
    '''执行信息编辑'''
    try:
        ob = User.objects.get(UserID=uid)
        ob.AdminState = request.POST['AdminState']
        ob.save()
        context = {"info": "修改成功！"}

    except Exception as err:
        print(err)
        context = {"info": "修改失败!"}
    return render(request, "myadmin/info.html", context)

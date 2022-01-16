from django.shortcuts import render
from django.http import HttpResponse
from myadmin.models import User
from django.core.paginator import Paginator
from django.db.models import Q  #或查询
from datetime import datetime
from web.models import Departmentprice


def index(request, pindex=1):
    '''浏览信息'''
    umod = Departmentprice.objects.all().order_by('-PriceTime')  #获取实例对象
    mywhere = []  #状态维持条件
    #获取并判断搜索条件
    kw = request.GET.get("keyword", None)
    ulist = umod.filter()
    if kw:
        ulist = umod.filter(
            Q(PriceTime__contains=kw) | Q(District__contains=kw))
        mywhere.append('keyword=' + kw)
    #执行分页处理
    pindex = int(pindex)
    upage = Paginator(ulist, 10)  #以每页五条数据分页
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
    #获取页码列表信息
    context = {
        "pricelist": list2,
        'plist': plist,
        'pindex': pindex,
        'maxpages': maxpages,
        'mywhere': mywhere
    }
    return render(request, "myadmin/price/index.html", context)

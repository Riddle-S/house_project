from django.shortcuts import render
from django.http import HttpResponse
from web.models import Departmentprice, Verifypricemessage
from data import forecast

# Create your views here.


#主页面视图函数
def index(request):
    return HttpResponse(forecast.forecast('上海'))

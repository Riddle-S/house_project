#前台子路由文件
from django.urls import path

from web.views import index, test

urlpatterns = [
    path('', index.index, name='web_index'),  #index文件中的index函数
    path('indexframe', index.indexframe, name='web_indexframe'),
    path('test', test.index),
    path('shanghaimap/<str:month>', index.shanghaimap, name='web_shanghaimap'),
    path('qushi', index.qushi, name='web_qushi'),
    path('indexframe2', index.indexframe2, name='web_indexframe2'),
    path('line/<str:district>/<str:year>', index.line, name='web_line')
]
handler404 = index.page_not_found

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from web.models import Departmentprice, Verifypricemessage
from pyecharts import options as opts
from pyecharts.charts import Map, Line
from pyecharts.globals import ThemeType
import pandas as pd
import json
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np

# Create your views here.


#主页面视图函数
def index(request):
    return render(request, 'web/index.html')


#主页面地图框架
def indexframe(request):
    df = pd.DataFrame(list(
        Departmentprice.objects.filter().values()))['PriceTime']  #转化为了series
    df = list(set(df))  #去重复值
    df.sort()  #不能在排序的同时进行赋值，否则为NONE
    context = {"PriceTime": df, "num": len(df)}
    return render(request, 'web/indexframe.html', context)


#主页面地图框架
def indexframe2(request):
    print("ok")
    df = pd.DataFrame(list(
        Departmentprice.objects.filter().values()))['PriceTime'].map(
            lambda x: x[0:4])  #转化为了series
    df = list(set(df))  #去重复值
    df.sort()  #不能在排序的同时进行赋值，否则为NONE
    district = pd.DataFrame(list(
        Departmentprice.objects.filter().values()))['District']  #转化为了series
    district = list(set(district))
    context = {
        "PriceTime": df,
        "num": len(df),
        "District": district,
        "num2": len(district)
    }
    return render(request, 'web/indexframe2.html', context)


#404页面
def page_not_found(request, exception):
    return render(request, 'web/404.html')


def qushi(request):
    return render(request, 'web/qushi.html')


def shanghaimap(request, month='2021-12-01'):
    #url中参数本身就是字符串形式，因此不需要在输入地址时加入单引号（单引号也会被处理成字符）
    df = pd.DataFrame(
        list(Departmentprice.objects.filter(
            PriceTime=month).values()))  #把sql数据转化为dataframe

    Districts = df['District']  #地区要用全称！（带上区）否则无法识别
    Prices = df['Price']
    data = [(district, price)
            for district, price in zip(Districts, Prices)]  #去掉上海市，否则无法识别
    c = Map()
    c.add("二手房房价", data, "上海", is_map_symbol_show=False)
    c.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    c.set_global_opts(
        title_opts=opts.TitleOpts(
            title="上海二手房房价",
            title_textstyle_opts=opts.TextStyleOpts(color='white')),
        visualmap_opts=opts.VisualMapOpts(
            max_=max(Prices),
            min_=min(Prices),
            is_piecewise=True,  # 设置为分段
            textstyle_opts=opts.TextStyleOpts(color="white"),
            pieces=[
                {
                    "max": 20000,
                    "min": 0,
                    "label": "0-20000",
                    # "color": "#FFE4E1"
                },
                {
                    "max": 40000,
                    "min": 20001,
                    "label": "20001-40000",
                    # "color": "#FF7F50"
                },
                {
                    "max": 60000,
                    "min": 40001,
                    "label": "40001-60000",
                    # "color": "#F08080"
                },
                {
                    "max": 80000,
                    "min": 60001,
                    "label": "60001-80000",
                    # "color": "#CD5C5C"
                },
                {
                    "max": 110000,
                    "min": 80001,
                    "label": ">=80001",
                    # "color": "#8B0000"
                }
            ],
        ),
        legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(
            color="white")),
        toolbox_opts=opts.ToolboxOpts(
            is_show=True,
            # orient="vertical",
            feature=opts.ToolBoxFeatureOpts(
                restore=opts.ToolBoxFeatureRestoreOpts(),
                data_view=opts.ToolBoxFeatureDataViewOpts(),
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                magic_type=opts.ToolBoxFeatureDataViewOpts(),
                brush=opts.ToolBoxFeatureDataZoomOpts(),
            )),

    )

    c.render(path="上海地图.html")
    # print(json.loads(c.dump_options()))
    return JsonResponse(json.loads(c.dump_options()),
                        content_type='application/json')


def line(request, district, year):
    print(district)
    print(year)
    df = pd.DataFrame(
        list(
            Departmentprice.objects.filter(District=district).filter(
                PriceTime__contains=year).values())).sort_values(
                    by='PriceTime', ascending=True)
    df.index = range(12)
    Month1 = df['PriceTime']
    Prices1 = df['Price']
    Month2 = df['PriceTime']
    Month2.loc[12] = str(int(year) + 1) + '-01-01'
    model = LinearRegression()
    x_train = np.array(range(12)).reshape(-1, 1)
    y_train = np.array(Prices1).reshape(-1, 1)

    x_pred = np.array(range(13)).reshape(-1, 1)
    model.fit(x_train, y_train)
    y_pred = model.predict(x_pred).astype(int)
    Prices2 = y_pred.flatten().tolist()  #flatten转为一维数组

    # print(Month, Prices)
    data1 = [(month1, price1) for month1, price1 in zip(Month1, Prices1)]
    data2 = [(month2, price2) for month2, price2 in zip(Month2, Prices2)]

    # print("Prices1")
    # print(Prices1)
    # print("Prices2")
    # print(Prices2)
    # print(Month1)
    # print(Month2)
    line = (Line().set_global_opts(
        tooltip_opts=opts.TooltipOpts(is_show=False),
        xaxis_opts=opts.AxisOpts(type_="category",
                                axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="white"))),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            axistick_opts=opts.AxisTickOpts(is_show=True),
            axisline_opts=opts.AxisLineOpts(linestyle_opts=opts.LineStyleOpts(color="white")),
            min_='dataMin',
        ),
        toolbox_opts=opts.ToolboxOpts(
            is_show=True,
            # orient="vertical",
            feature=opts.ToolBoxFeatureOpts(
                restore=opts.ToolBoxFeatureRestoreOpts(),
                data_view=opts.ToolBoxFeatureDataViewOpts(),
                data_zoom=opts.ToolBoxFeatureDataZoomOpts(),
                magic_type=opts.ToolBoxFeatureDataViewOpts(),
                brush=opts.ToolBoxFeatureDataZoomOpts(),
            )),
        legend_opts=opts.LegendOpts(textstyle_opts=opts.TextStyleOpts(
            color="white")),
        
        title_opts=opts.TitleOpts(
            title=district + year + "年二手房房价变化曲线",
            title_textstyle_opts=opts.TextStyleOpts(color='white')),
    ).add_xaxis(xaxis_data=Month2).add_yaxis(
        series_name="变化曲线",
        y_axis=Prices1,
        symbol="emptyCircle",
        symbol_size=8,
        linestyle_opts=opts.LineStyleOpts(width=3,opacity=1),
        is_symbol_show=True,
        is_connect_nones=True,
        label_opts=opts.LabelOpts(is_show=False),
        color="yellow",
    ).add_yaxis(
        series_name="预测曲线",
        y_axis=Prices2,
        symbol="emptyCircle",
        symbol_size=8,
        linestyle_opts=opts.LineStyleOpts(width=3,opacity=1),
        is_symbol_show=True,
        is_connect_nones=True,
        label_opts=opts.LabelOpts(is_show=False),
        
    ))
    line.render(path='pyecharts-line.html')
    return HttpResponse(json.dumps(json.loads(line.dump_options()),
                                   ensure_ascii=False),
                        content_type="application/json charset=utf-8")

# 2019ncov_data_visualization
2019ncov data visualization based on Pyecharts&amp;Flask
新冠肺炎疫情实时监控
基于 Pyecharts 和 Flask 的新冠肺炎疫情数据的可视化项目
一、项目背景
2020 年伊始，一种新型冠状病毒引发肺炎疫情，在春运的庞大人流下从国内首先报告
地武汉席卷全国并蔓延全球。在几个月的时间里，新冠病毒在全球感染超过 300 万人，并夺
去超过 20 万人的生命。虽然当下国内的疫情已经得到了控制，但在肺炎疫情依然在国外肆
虐的大环境下，我国的疫情防控依然任重道远。在使用大数据进行疫情的联防联控的今天，
不少互联网厂商开始提供疫情实时数据的页面供公众查询，也提供对应的 API 供二次开发。
本项目使用 Pyecharts 和 Flask，使用腾讯提供的 API 进行国内实时疫情数据可视化和初步
分析。
二、数据来源和版权
本 项 目 所 使 用 的 实 时 数 据 来 源 于 腾 讯 国 内 疫 情 数 据 API ， 接 口 地 址 为 ：
https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5 ， 数 可 与 腾 讯 官 方 网 站
https://xw.qq.com/act/qgfeiyan 中显示的国内数据相对应。本项目使用的所有数据仅供
学习交流之用，数据版权归属为腾讯或与数据相关的实体。
本项目所有代码均在 GPL3.0 许可证下开源，可在 GitHub 上找到本项目的所有代码：
https://github.com/JYH1999/2019ncov_data_visualization。本项目已被部署于一台服务
器，访问链接 http://ncov.privcloud.cn:5000/查看项目效果。
三、项目架构
本项目在实现上由 get_api.py,pyecharts_drawing.py 和 flask_framework.py 组成。
get_api.py 为供 pyecharts_drawing.py 调用的函数库，pyecharts_drawing.py 为根据 API
数据生成对应图表 HTML 文件的程序，flask_framework.py 为一个简易的 web 框架，用于提
供 HTML 静态页面的路由服务，并支持 HTML 文件的热更新。
本项目在文件组成上由 get_api.py,pyecharts_drawing.py,flask_framework.py 程序
文件，data_demo.json 的 json 格式 API 返回示例文件和 templates,config_json 两个文件
夹组成。templates 和 config_json 文件夹下分别存放用于 Flask 路由的目标 HTML 文件和
用于 Pyecharts 进行图标拼合成 Page 的格式文件。
四、代码分析
4.1 data_demo.json 分析
项目提供data_demo.json文件，内存放某时刻从腾讯国内疫情数据API中获取的数据。
经过 VSCode 初步格式化，其组成如图所示：
图中内容易得，腾讯 API 中提供的数据的'data'项内存在疫情的相关信息，而'ret'项
中无任何有效数据。故在项目中舍去'ret'中的内容，仅使用'data'中的数据。
4.2 get_api.py 分析
1. import requests
2. import json
get_api.py 为供 pyecharts_drawing.py 使用函数库，提供从 API 获取信息的功能。为
了从 API 中获取信息，需要使用 requests 库发送 http/https 请求；为了解码 API 中的数
据，需要使用 json 库。
1. def get_api_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disea
se_h5'):#请求 api 函数，返回疫情数据字典
2. response=requests.get(api_url)
3. api_json=response.json()
4. api_status_code=response.status_code
5. if api_status_code!='200':
6. api_data=json.loads(api_json['data'])
7. return api_data
8. else:
9. return 0
get_api.py 内定义 get_api_dict()函数，带有一个含默认 url 的形参，用于获取来自
腾讯疫情数据 API 的原始信息。从 API 中获得的数据被放入 response 变量中，并使用 json
库解码后转移入 api_json 变量。api_status_code 获取 response 中的 status_code 存入变
量中。函数内使用 if 进行数据获取状态检测，在 status_code 为 200 时返回将原始 json 中
'data'解码为字典的数据 api_data，否则返回 0。
1. def get_total_confirm_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?
name=disease_h5'):#获取分省感染人数总计函数，返回字典
2. original_dict=get_api_dict(api_url)
3. total_confirm_dict={}
4. total_confirm_dict[original_dict['areaTree'][0]['name']]=original_dict['
areaTree'][0]['total']['confirm']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. total_confirm_dict[items['name']]=items['total']['confirm']
7. return total_confirm_dict
get_api.py 内定义 get_total_confirm_dict()函数，带有一个含默认 url 的形参，用
于获取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省感染人数总计的字典。函数
使用 get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提
取分省数据合并为字典返回。
1. def get_today_confirm_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?
name=disease_h5'):#获取分省当日感染人数，返回字典
2. original_dict=get_api_dict(api_url)
3. today_confirm_dict={}
4. today_confirm_dict[original_dict['areaTree'][0]['name']]=original_dict['
areaTree'][0]['today']['confirm']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. today_confirm_dict[items['name']]=items['today']['confirm']
7. return today_confirm_dict
get_api.py 内定义 get_today_confirm_dict()函数，带有一个含默认 url 的形参，用
于获取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省当日感染人数的字典。函数
使用 get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提
取分省数据合并为字典返回。
1. def get_total_no_infect_num(api_url='https://view.inews.qq.com/g2/getOnsInfo
?name=disease_h5'):#获取全国无症状感染者总人数，返回值
2. original_dict=get_api_dict(api_url)
3. total_no_infect=original_dict['chinaTotal']['noInfect']#获取数据
4. return total_no_infect
get_api.py 内定义 get_total_no_infect_num()函数，带有一个含默认 url 的形参，用
于获取来自腾讯疫情数据 API 的原始信息，并从中提取全国无症状感染者总人数。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国无症状感染者人数数值，并返
回。
1. def get_today_no_infect_num(api_url='https://view.inews.qq.com/g2/getOnsInfo
?name=disease_h5'):#获取全国今日无症状感染者人数，返回值
2. original_dict=get_api_dict(api_url)
3. today_no_infect=original_dict['chinaAdd']['noInfect']#获取数据
4. return today_no_infect
get_api.py 内定义 get_today_no_infect_num()函数，带有一个含默认 url 的形参，用
于获取来自腾讯疫情数据 API 的原始信息，并从中提取全国今日无症状感染者人数。函数使
用 get_api_dict()函数获取 API 原始数据字典，从中提取全国今日无症状感染者人数数值，
并返回。
1. def get_today_death_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?nam
e=disease_h5'):#获取全国今日死亡人数，返回值
2. original_dict=get_api_dict(api_url)
3. today_death=original_dict['chinaAdd']['dead']#获取全国数据
4. return today_death
get_api.py 内定义 get_today_death_num()函数，带有一个含默认 url 的形参，用于获
取来自腾讯疫情数据 API 的原始信息，并从中提取全国今日死亡人数。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国今日因新冠肺炎死亡人数数值，
并返回。
1. def get_total_death_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?na
me=disease_h5'):#获取分省死亡人数总计，返回字典
2. original_dict=get_api_dict(api_url)
3. total_death_dict={}
4. total_death_dict[original_dict['areaTree'][0]['name']]=original_dict['ar
eaTree'][0]['total']['dead']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. total_death_dict[items['name']]=items['total']['dead']
7. return total_death_dict
get_api.py 内定义 get_total_death_dict()函数，带有一个含默认 url 的形参，用于
获取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省死亡人数总计的字典。函数使
用 get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提取
分省数据合并为字典返回。
1. def get_heal_rate_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name
=disease_h5'):#获取分省治愈率统计，返回字典
2. original_dict=get_api_dict(api_url)
3. heal_rate_dict={}
4. heal_rate_dict[original_dict['areaTree'][0]['name']]=original_dict['area
Tree'][0]['total']['healRate']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. heal_rate_dict[items['name']]=items['total']['healRate']
7. return heal_rate_dict
get_api.py 内定义 get_heal_rate_dict()函数，带有一个含默认 url 的形参，用于获
取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省治愈率统计的字典。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提取分省
数据合并为字典返回。
1. def get_death_rate_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?nam
e=disease_h5'):#获取分省死亡率统计，返回字典
2. original_dict=get_api_dict(api_url)
3. death_rate_dict={}
4. death_rate_dict[original_dict['areaTree'][0]['name']]=original_dict['are
aTree'][0]['total']['deadRate']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. death_rate_dict[items['name']]=items['total']['deadRate']
7. return death_rate_dict
get_api.py 内定义 get_death_rate_dict()函数，带有一个含默认 url 的形参，用于获
取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省死亡率统计的字典。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提取分省
数据合并为字典返回。
1. def get_today_heal_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?name
=disease_h5'):#获取当日全国治愈人数，返回值
2. original_dict=get_api_dict(api_url)
3. today_heal=original_dict['chinaAdd']['heal']#获取全国数据
4. return today_heal
get_api.py 内定义 get_today_heal_num()函数，带有一个含默认 url 的形参，用于获
取来自腾讯疫情数据 API 的原始信息，并从中提取全国今日治愈人数。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国今日新冠肺炎治愈人数数值，并
返回。
1. def get_total_heal_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?nam
e=disease_h5'):#获取分省治愈人数统计，返回字典
2. original_dict=get_api_dict(api_url)
3. total_heal_dict={}
4. total_heal_dict[original_dict['areaTree'][0]['name']]=original_dict['are
aTree'][0]['total']['heal']#获取全国数据
5. for items in original_dict['areaTree'][0]['children']:#分省获取
6. total_heal_dict[items['name']]=items['total']['heal']
7. return total_heal_dict
get_api.py 内定义 get_total_heal_dict()函数，带有一个含默认 url 的形参，用于获
取来自腾讯疫情数据 API 的原始信息，并从中提取含有分省治愈人数统计的字典。函数使用
get_api_dict()函数获取 API 原始数据字典，从中提取全国数据，并使用 for 循环提取分省
数据合并为字典返回。
1. def get_data_update_time(api_url='https://view.inews.qq.com/g2/getOnsInfo?na
me=disease_h5'):#获取数据更新时间，返回字符串
2. original_dict=get_api_dict(api_url)
3. data_update_time=original_dict['lastUpdateTime']
4. return data_update_time
get_api.py 内定义 get_data_update_time()函数，带有一个含默认 url 的形参，用于
获取来自腾讯疫情数据 API 的原始信息，并从中提取腾讯疫情数据的最后更新时间字符串，
并返回。
4.3 pyecharts_drawing.py 分析
1. import get_api
2. from pyecharts.charts import Map,Geo
3. import pyecharts.options as opts
4. from pyecharts.charts import Gauge
5. from pyecharts.charts import Bar
6. from pyecharts.commons.utils import JsCode
7. from pyecharts.globals import ThemeType
8. from pyecharts.charts import Pie
9. from pyecharts.faker import Faker
10. from pyecharts.charts import Liquid
11. from pyecharts.charts import Tab,Page,Grid
12. import time
pyecharts_drawing.py 为根据 API 数据生成对应图表 HTML 文件的程序，主要实现疫情
数据可视化图表的绘制。由于 pyecharts_drawing.py 需要获取 API 数据，程序调用了
get_api.py。程序导入了pyecharts库中Map,Geo,Gauge,Bar,Pie,Liquid等不同的绘图库，
并导入了 opts,Faker,ThemeType,JsCode 等设置库，同时导入了 Tab,Page,Grid 等图形组合
库。为了实现定时更新疫情数据可视化 HTML 的功能，程序导入 time 时间库。
api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'#api 地址
虽然 get_api.py 中的函数均默认定义了传入实参的默认值，但出于代码严谨性和后期
更改 API 地址的便利性， pyecharts_drawing.py 定义全局变量 api_url，用于向各个函数
提供 API 地址。
1. def get_total_confirm_map():
2. total_confirm_dict=get_api.get_total_confirm_dict(api_url)#分省统计确诊患
者总数字典
3. total_confirm_list=[[x,total_confirm_dict[x]] for x in list(total_confir
m_dict)]#分省统计确诊患者总数列表
4. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
5. total_confirm_map=(#全国确诊统计图
6. Map(init_opts=opts.InitOpts())
7. .add("确诊患者",total_confirm_list,"china")
8. .set_global_opts(
9. title_opts=opts.TitleOpts(title="各省累计确诊患者数",subtitle="数
据更新时间：
{}".format(data_update_time),pos_right="center",pos_top="5%",title_link='/no
w_page/',title_target='self'),
10. visualmap_opts=opts.VisualMapOpts(max_=1500),
11. legend_opts=opts.LegendOpts(is_show=False)
12. )
13. )
14. total_confirm_map.chart_id='totalconfirmmap'
15. return total_confirm_map
pyecharts_drawing.py 中定义 get_total_confirm_map()函数，使用 get_api.py 中的
get_total_confirm_dict() 函 数 提 供 的 数 据 绘 制 全 国 疫 情 确 诊 统 计 地 图 ， 使 用
get_data_update_time()函数获取数据的更新时间信息。为了使颜色分区更加明显，经过调
试后决定设置 1500 作为感染人数最大值的标定量。同时，函数生成的图表标题内嵌超链接，
用于配合 flask_framework.py 构成图表之间的切换。为了便于后期组合，该图设置了
chart_id。函数返回一个 Map 对象。
1. def get_total_death_rate_bar():
2. death_rate_dict=get_api.get_death_rate_dict(api_url)#分省死亡率字典
3. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
4. total_death_rate_bar = (#各省死亡率图
5. Bar()
6. .add_xaxis(list(death_rate_dict.keys())[1:])
7. .add_yaxis("死亡
率%", [float(x) for x in death_rate_dict.values()][1:],color='red')
8. .set_global_opts(
9. xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-
60)),
10. title_opts=opts.TitleOpts(title="各省新冠肺炎患者死亡率
(%)",subtitle="数据更新时间：
{}".format(data_update_time),pos_top="0%",pos_left='center'),
11. yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter
="{value}%")),
12. legend_opts=opts.LegendOpts(is_show=False)
13. )
14. .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
15. )
16. total_death_rate_bar.chart_id='totaldeathratebar'
17. return total_death_rate_bar
pyecharts_drawing.py 中定义 get_total_death_rate_bar()函数，使用 get_api.py 中
的 get_death_rate_dict()函数提供的数据绘制各省新冠肺炎死亡率条形统计图，使用
get_data_update_time()函数获取数据的更新时间信息。由于省份数量较多，为了完全显示
每个省份的数量，本图将省份的名称旋转 60 度以节省 x 向空间。为了便于后期组合，该图
设置了 chart_id。函数返回一个 Bar 对象。
1. def get_now_confirm_pie():
2. now_confirm_dict=get_api.get_now_confirm_dict(api_url)#分省剩余确诊患者字
典
3. now_confirm_list=[[x,now_confirm_dict[x]] for x in list(now_confirm_dict
) if now_confirm_dict[x]!=0 ]#分省剩余确诊患者列表（省略无患者省份）
4. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
5. now_confirm_pie = (#当前确诊患者地域分布饼图
6. Pie(init_opts=opts.InitOpts(width="400px", height="400px"))
7. .add("", now_confirm_list[1:],center=["45%", "60%"],)
8. .set_global_opts(
9. title_opts=opts.TitleOpts(title="当前确诊患者地域分布",subtitle="
数据更新时间：{}".format(data_update_time),pos_left="30%",pos_top="0%"),
10. legend_opts=opts.LegendOpts(orient="vertical",pos_left="85%",pos
_top='15%')
11. )
12. .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
13. )
14. now_confirm_pie.chart_id='nowconfirmpie'
15. return now_confirm_pie
pyecharts_drawing.py 中定义 get_now_confirm_pie()函数，使用 get_api.py 中的
get_now_confirm_dict()函数提供的数据绘制分省当前剩余确诊患者分布饼图。由于省份数
量较多，本图将图注设置为纵向排列。为了便于后期组合，该图设置了 chart_id。函数返回
一个 Pie 对象。
1. def get_national_heal_rate_liquid():
2. heal_rate_dict=get_api.get_heal_rate_dict(api_url)#分省治愈率字典
3. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
4. national_heal_rate_liquid = (#全国治愈率 liquid 图
5. Liquid(init_opts=opts.InitOpts(width="400px", height="400px"))
6. .add("治愈率", [float(heal_rate_dict['中国
'])/100], is_outline_show=False,center=["35%", "40%"],
7. label_opts=opts.LabelOpts(
8. font_size=50,
9. formatter=JsCode(
10. """function (param) {
11. return (Math.floor(param.value * 10000) / 100) + '%'
;
12. }"""
13. ),
14. position="inside",
15. )
16. )
17. .set_global_opts(title_opts=opts.TitleOpts(title="新冠肺炎全国治愈率
",title_link='/heal_page/',title_target='self',subtitle="数据更新时间：
{}".format(data_update_time),pos_left="15%",pos_top="0%"))
18. )
19. national_heal_rate_liquid.chart_id='nationalhealrateliquid'
20. return national_heal_rate_liquid
pyecharts_drawing.py 中定义 get_national_heal_rate_liquid() 函 数 ， 使 用
get_api.py 中的 get_heal_rate_dict()函数提供的数据绘制全国治愈率水滴图。为使治愈
率显示更为精确，图中使用了 JsCode 内嵌了 JavaScript 语句对数据进行格式化。同时，函
数生成的图表标题内嵌超链接，用于配合 flask_framework.py 构成图表之间的切换。为了
便于后期组合，该图设置了 chart_id。函数返回一个 Liquid 对象。
1. def get_now_confirm_map():
2. now_confirm_dict=get_api.get_now_confirm_dict(api_url)#分省剩余确诊患者字
典
3. now_confirm_list_with_all_province=[[x,now_confirm_dict[x]] for x in lis
t(now_confirm_dict)]#分省剩余确诊患者列表
4. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
5. now_confirm_map=(#全国剩余确诊统计图
6. Map(init_opts=opts.InitOpts())
7. .add("确诊患者",now_confirm_list_with_all_province,"china")
8. .set_global_opts(
9. title_opts=opts.TitleOpts(title="当前各省确诊患者数",subtitle="数
据更新时间：
{}".format(data_update_time),pos_right="center",pos_top="5%",title_link='/',
title_target='self'),
10. visualmap_opts=opts.VisualMapOpts(max_=50),
11. legend_opts=opts.LegendOpts(is_show=False)
12. )
13. )
14. now_confirm_map.chart_id='nowconfirmmap'
15. return now_confirm_map
pyecharts_drawing.py 中定义 get_now_confirm_map()函数，使用 get_api.py 中的
get_now_confirm_dict()函数提供的数据绘制全国疫情剩余确诊数统计地图。为了使颜色分
区更加明显，经过调试后决定设置 50 作为感染人数最大值的标定量。同时，函数生成的图
表标题内嵌超链接，用于配合 flask_framework.py 构成图表之间的切换。为了便于后期组
合，该图设置了 chart_id。函数返回一个 Map 对象。
1. def get_national_death_rate_liquid():
2. death_rate_dict=get_api.get_death_rate_dict(api_url)#分省死亡率字典
3. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
4. national_death_rate_liquid = (#全国死亡率 liquid 图
5. Liquid(init_opts=opts.InitOpts(width="400px", height="400px"))
6. .add("死亡率", [float(death_rate_dict['中国
'])/100], is_outline_show=False,center=["35%", "40%"],
7. label_opts=opts.LabelOpts(
8. font_size=50,
9. formatter=JsCode(
10. """function (param) {
11. return (Math.floor(param.value * 10000) / 100) +
'%';
12. }"""
13. ),
14. position="inside"
15. )
16. )
17. .set_global_opts(title_opts=opts.TitleOpts(title="新冠肺炎全国死亡率
",title_link='/death_page/',title_target='self',subtitle="数据更新时间：
{}".format(data_update_time),pos_left="15%",pos_top="0%"))
18. )
19. national_death_rate_liquid.chart_id='nationaldeathrateliquid'
20. return national_death_rate_liquid
pyecharts_drawing.py 中 定 义 get_national_death_rate_liquid() 函 数 ， 使 用
get_api.py 中的 get_death_rate_dict()函数提供的数据绘制全国死亡率水滴图。为使死亡
率显示更为精确，图中使用了 JsCode 内嵌了 JavaScript 语句对数据进行格式化。同时，函
数生成的图表标题内嵌超链接，用于配合 flask_framework.py 构成图表之间的切换。为了
便于后期组合，该图设置了 chart_id。函数返回一个 Liquid 对象。
1. def get_total_heal_rate_bar():
2. data_update_time=get_api.get_data_update_time(api_url)#api 数据更新时间
3. heal_rate_dict=get_api.get_heal_rate_dict(api_url)#分省治愈率字典
4. total_heal_rate_bar = (#各省治愈率图
5. Bar()
6. .add_xaxis(list(heal_rate_dict.keys())[1:])
7. .add_yaxis("治愈
率%", [float(x) for x in heal_rate_dict.values()][1:],color='green')
8. .set_global_opts(
9. xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-
60)),
10. title_opts=opts.TitleOpts(title="各省新冠肺炎患者治愈率
(%)",subtitle="数据更新时间：
{}".format(data_update_time),pos_top="0%",pos_left='center'),
11. yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter
="{value}%")),
12. legend_opts=opts.LegendOpts(is_show=False)
13. )
14. .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
15. )
16. total_heal_rate_bar.chart_id='totalhealratebar'
17. return total_heal_rate_bar
pyecharts_drawing.py 中定义 get_total_heal_rate_bar()函数，使用 get_api.py 中
的 get_heal_rate_dict()函数提供的数据绘制各省新冠肺炎患者治愈率条形统计图，使用
get_data_update_time()函数获取数据的更新时间信息。由于省份数量较多，为了完全显示
每个省份的数量，本图将省份的名称旋转 60 度以节省 x 向空间。为了便于后期组合，该图
设置了 chart_id。函数返回一个 Bar 对象。
1. def get_today_confirm_gauge():
2. today_confirm_dict=get_api.get_today_confirm_dict(api_url)#分省统计当日确
诊患者字典
3. today_confirm_gauge=(#今日确诊仪表盘
4. Gauge()
5. .add(series_name="今日确诊", data_pair=[["今日确诊
", int(today_confirm_dict['中国
'])]],detail_label_opts=opts.LabelOpts(formatter="{value}人"))
6. .set_global_opts(
7. legend_opts=opts.LegendOpts(is_show=False),
8. tooltip_opts=opts.TooltipOpts(is_show=False, formatter="{a} <br/
>{b} : {c}人"),
9. )
10. )
11. today_confirm_gauge.chart_id='todayconfirmgauge'
12. return today_confirm_gauge
pyecharts_drawing.py 中定义 get_today_confirm_gauge()函数，使用 get_api.py 中
的 get_today_confirm_dict()函数提供的数据绘制今日确证患者数仪表盘。为了便于后期
组合，该图设置了 chart_id。函数返回一个 Gauge 对象。
1. def get_today_no_infect_gauge():
2. today_no_infect_num=get_api.get_today_no_infect_num(api_url)#获取当日无症
状感染者
3. today_no_infect_gauge=(#今日无症状仪表
4. Gauge()
5. .add(series_name="今日无症状", data_pair=[["今日无症状
", int(today_no_infect_num)]],detail_label_opts=opts.LabelOpts(formatter="{v
alue}人"))
6. .set_global_opts(
7. legend_opts=opts.LegendOpts(is_show=False),
8. tooltip_opts=opts.TooltipOpts(is_show=False, formatter="{a} <br/
>{b} : {c}人"),
9. )
10. )
11. today_no_infect_gauge.chart_id='todaynoinfectgauge'
12. return today_no_infect_gauge
pyecharts_drawing.py 中定义 get_today_no_infect_gauge()函数，使用 get_api.py
中的 get_today_no_incfect_num()函数提供的数据绘制今日确证患者数仪表盘。为了便于
后期组合，该图设置了 chart_id。函数返回一个 Gauge 对象。
1. while True:
2. main_page=Page(layout=Page.DraggablePageLayout)
3. main_page.add(
4. get_total_confirm_map(),
5. get_national_heal_rate_liquid(),
6. get_national_death_rate_liquid(),
7. get_today_confirm_gauge(),
8. get_today_no_infect_gauge(),
9. )
10. main_page.render('main_page_temp.html')
11. Page.save_resize_html('main_page_temp.html',cfg_file='./config_json/main
_page.json',dest='./templates/main_page.html')
12. now_page=Page(layout=Page.DraggablePageLayout)
13. now_page.add(
14. get_now_confirm_map(),
15. get_now_confirm_pie()
16. )
17. now_page.render('now_page_temp.html')
18. Page.save_resize_html('now_page_temp.html',cfg_file='./config_json/now_p
age.json',dest='./templates/now_page.html')
19. heal_page=Page(layout=Page.DraggablePageLayout)
20. heal_page.add(
21. get_national_heal_rate_liquid(),
22. get_total_heal_rate_bar()
23. )
24. heal_page.render('heal_page_temp.html')
25. Page.save_resize_html('heal_page_temp.html',cfg_file='./config_json/heal
_page.json',dest='./templates/heal_page.html')
26. death_page=Page(layout=Page.DraggablePageLayout)
27. death_page.add(
28. get_national_death_rate_liquid(),
29. get_total_death_rate_bar()
30. )
31. death_page.render('death_page_temp.html')
32. Page.save_resize_html('death_page_temp.html',cfg_file='./config_json/dea
th_page.json',dest='./templates/death_page.html')
33. time.sleep(60)
pyecharts_drawing.py 中构建了无限循环，用于配合循环末尾的 time.sleep()函数形
成 实 现 定 时 （ 60s ） 刷 新 功 能 。 循 环 结 构 内 部 构 建 4 个 Page 对 象 ， 分 别 为
main_page,now_page,heal_page 和 death_page，用于生成对应展示网页的 HTML 文件。每个
Page 对象根据功能的不同（主要信息、当前疫情信息、治愈率信息和死亡率信息）组合
pyecharts_drawing.py 中的不同图表构成 DraggablePage 对象，渲染为带有_temp 的 HTML
文件，经过人工排版后将对应的排版数据保存入 config_json 文件夹中。最后调用
Page.save_resize_html()函数渲染用于 Flask 路由的 html 文件，存入 templates 文件夹
中。
4.3 flask_framework.py 分析
1. from flask import Flask
2. from flask import render_template
3. app = Flask(__name__)
flask_framework.py 为项目提供 Flask 框架，实现路由功能。程序需要导入 Flask 框
架以及对应的 HTML 渲染模块。程序创建一个标准的 Flask app。
1. app.jinja_env.auto_reload = True
2. app.config['TEMPLATES_AUTO_RELOAD'] = True
flask_framework.py 对所生成 app 内置的 jinja 模板引擎进行设置，使 app 支持 HTML
的热更新，满足 pyecharts_drawing.py 的每分钟更新 HTML 特性。
1. @app.route('/')
2. def main_page():
3. return render_template('main_page.html')
4.
5. @app.route('/main_page/')
6. def main_page_back():
7. return render_template('main_page.html')
8.
9. @app.route('/now_page/')
10. def now_page():
11. return render_template('now_page.html')
12.
13. @app.route('/heal_page/')
14. def heal_page():
15. return render_template('heal_page.html')
16.
17. @app.route('/death_page/')
18. def death_page():
19. return render_template('death_page.html')
flask_framework.py 内定义了一系列由 app.route()装饰后的函数，用于提供基本的
路由服务和网页渲染服务。代码与 pyecharts_drawing.py 中图表标题内置的超链接相匹配，
实现网页内点击跳转的功能。同时，单独加入/main_page/跳转定义，用于用户对于链接输
入的快捷访问，同时便于理解和记忆。
1. if __name__ == '__main__':
2. app.run(host='0.0.0.0',port= 5000)#执行 flask 的运行
flask_framework.py 的运行部分，该代码将实现在 Linux 服务器的 5000 端口上提供
flask 服务的功能。在 Windows 本地调试或实现时，可更改 host 为 127.0.0.1。若经过网站
备案，可调整 port 为 80 便于实现 HTTP 访问。
五、项目实现展示
通过服务器的合理配置，本项目可实现以下效果：
输入部署的服务器 ip 地址或域名，打开项目主页：
点击“各省累计确诊患者数”标题，进入当日疫情数据界面：
点击“新冠肺炎全国治愈率”标题，进入新冠肺炎治愈率统计页面：
点击“新冠肺炎全国死亡率”标题，进入新冠肺炎死亡率统计页面：
以上网页展示的数据均会根据腾讯 API 数据的更新而自动更新，实现实时监测的功能。
项目的目标功能得到实现。

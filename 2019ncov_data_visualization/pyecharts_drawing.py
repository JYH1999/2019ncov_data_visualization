#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  pyecharts_drawing.py
#  
#  Copyright 2020 金煜航 <jinyuhang@whut.edu.cn>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 3 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  
import get_api
from pyecharts.charts import Map,Geo
import pyecharts.options as opts
from pyecharts.charts import Gauge
from pyecharts.charts import Bar
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from pyecharts.charts import Pie
from pyecharts.faker import Faker
from pyecharts.charts import Liquid
from pyecharts.charts import Tab,Page,Grid
import time
api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'#api地址

def get_total_confirm_map():
    total_confirm_dict=get_api.get_total_confirm_dict(api_url)#分省统计确诊患者总数字典
    total_confirm_list=[[x,total_confirm_dict[x]] for x in list(total_confirm_dict)]#分省统计确诊患者总数列表
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    total_confirm_map=(#全国确诊统计图
        Map(init_opts=opts.InitOpts())
        .add("确诊患者",total_confirm_list,"china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="各省累计确诊患者数",subtitle="数据更新时间：{}".format(data_update_time),pos_right="center",pos_top="5%",title_link='/now_page/',title_target='self'),
            visualmap_opts=opts.VisualMapOpts(max_=1500),
            legend_opts=opts.LegendOpts(is_show=False)
        ) 
    )
    total_confirm_map.chart_id='totalconfirmmap'
    return total_confirm_map
#get_total_confirm_map().render('total_confirm_map.html')
def get_total_death_rate_bar():
    death_rate_dict=get_api.get_death_rate_dict(api_url)#分省死亡率字典
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    total_death_rate_bar = (#各省死亡率图
        Bar()
        .add_xaxis(list(death_rate_dict.keys())[1:])
        .add_yaxis("死亡率%", [float(x) for x in death_rate_dict.values()][1:],color='red')
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)),
            title_opts=opts.TitleOpts(title="各省新冠肺炎患者死亡率(%)",subtitle="数据更新时间：{}".format(data_update_time),pos_top="0%",pos_left='center'), 
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    total_death_rate_bar.chart_id='totaldeathratebar'
    return total_death_rate_bar
#get_total_death_rate_bar().render("death_rate_bar.html")
def get_now_confirm_pie():
    now_confirm_dict=get_api.get_now_confirm_dict(api_url)#分省剩余确诊患者字典
    now_confirm_list=[[x,now_confirm_dict[x]] for x in list(now_confirm_dict) if now_confirm_dict[x]!=0 ]#分省剩余确诊患者列表（省略无患者省份）
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    now_confirm_pie = (#当前确诊患者地域分布饼图
        Pie(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add("", now_confirm_list[1:],center=["45%", "60%"],)
        .set_global_opts(
            title_opts=opts.TitleOpts(title="当前确诊患者地域分布",subtitle="数据更新时间：{}".format(data_update_time),pos_left="30%",pos_top="0%"),
            legend_opts=opts.LegendOpts(orient="vertical",pos_left="85%",pos_top='15%')
        )
        .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    )
    now_confirm_pie.chart_id='nowconfirmpie'
    return now_confirm_pie
#get_now_confirm_pie().render("now_confirm_pie.html")
def get_national_heal_rate_liquid():
    heal_rate_dict=get_api.get_heal_rate_dict(api_url)#分省治愈率字典
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    national_heal_rate_liquid = (#全国治愈率liquid图
        Liquid(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add("治愈率", [float(heal_rate_dict['中国'])/100], is_outline_show=False,center=["35%", "40%"],
            label_opts=opts.LabelOpts(
                font_size=50,
                formatter=JsCode(
                    """function (param) {
                        return (Math.floor(param.value * 10000) / 100) + '%';
                    }"""
                ),
                position="inside",
            )
        )
        .set_global_opts(title_opts=opts.TitleOpts(title="新冠肺炎全国治愈率",title_link='/heal_page/',title_target='self',subtitle="数据更新时间：{}".format(data_update_time),pos_left="15%",pos_top="0%"))
    )
    national_heal_rate_liquid.chart_id='nationalhealrateliquid'
    return national_heal_rate_liquid
#get_national_heal_rate_liquid().render("national_heal_rate_liquid.html")
def get_now_confirm_map():
    now_confirm_dict=get_api.get_now_confirm_dict(api_url)#分省剩余确诊患者字典
    now_confirm_list_with_all_province=[[x,now_confirm_dict[x]] for x in list(now_confirm_dict)]#分省剩余确诊患者列表
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    now_confirm_map=(#全国剩余确诊统计图
        Map(init_opts=opts.InitOpts())
        .add("确诊患者",now_confirm_list_with_all_province,"china")
        .set_global_opts(
            title_opts=opts.TitleOpts(title="当前各省确诊患者数",subtitle="数据更新时间：{}".format(data_update_time),pos_right="center",pos_top="5%",title_link='/',title_target='self'),
            visualmap_opts=opts.VisualMapOpts(max_=50),
            legend_opts=opts.LegendOpts(is_show=False)
        ) 
    )
    now_confirm_map.chart_id='nowconfirmmap'
    return now_confirm_map
#get_now_confirm_map().render('now_confirm_map.html')
def get_national_death_rate_liquid():
    death_rate_dict=get_api.get_death_rate_dict(api_url)#分省死亡率字典
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    national_death_rate_liquid = (#全国死亡率liquid图
        Liquid(init_opts=opts.InitOpts(width="400px", height="400px"))
        .add("死亡率", [float(death_rate_dict['中国'])/100], is_outline_show=False,center=["35%", "40%"],
                label_opts=opts.LabelOpts(
                    font_size=50,
                    formatter=JsCode(
                        """function (param) {
                            return (Math.floor(param.value * 10000) / 100) + '%';
                        }"""
                    ),
                    position="inside"
                )
            )
        .set_global_opts(title_opts=opts.TitleOpts(title="新冠肺炎全国死亡率",title_link='/death_page/',title_target='self',subtitle="数据更新时间：{}".format(data_update_time),pos_left="15%",pos_top="0%"))
    )
    national_death_rate_liquid.chart_id='nationaldeathrateliquid'
    return national_death_rate_liquid
#get_national_death_rate_liquid().render("national_death_rate_liquid.html")
def get_total_heal_rate_bar():
    data_update_time=get_api.get_data_update_time(api_url)#api数据更新时间
    heal_rate_dict=get_api.get_heal_rate_dict(api_url)#分省治愈率字典
    total_heal_rate_bar = (#各省治愈率图
        Bar()
        .add_xaxis(list(heal_rate_dict.keys())[1:])
        .add_yaxis("治愈率%", [float(x) for x in heal_rate_dict.values()][1:],color='green')
        .set_global_opts(
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=-60)),
            title_opts=opts.TitleOpts(title="各省新冠肺炎患者治愈率(%)",subtitle="数据更新时间：{}".format(data_update_time),pos_top="0%",pos_left='center'), 
            yaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(formatter="{value}%")),
            legend_opts=opts.LegendOpts(is_show=False)
        )
        .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    )
    total_heal_rate_bar.chart_id='totalhealratebar'
    return total_heal_rate_bar
#get_total_heal_rate_bar().render("heal_rate_bar.html")
def get_today_confirm_gauge():
    today_confirm_dict=get_api.get_today_confirm_dict(api_url)#分省统计当日确诊患者字典
    today_confirm_gauge=(#今日确诊仪表盘
        Gauge()
        .add(series_name="今日确诊", data_pair=[["今日确诊", int(today_confirm_dict['中国'])]],detail_label_opts=opts.LabelOpts(formatter="{value}人"))
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=False, formatter="{a} <br/>{b} : {c}人"),
        )
    )
    today_confirm_gauge.chart_id='todayconfirmgauge'
    return today_confirm_gauge
#get_today_confirm_gauge().render("today_confirm_gauge.html")
def get_today_no_infect_gauge():
    today_no_infect_num=get_api.get_today_no_infect_num(api_url)#获取当日无症状感染者
    today_no_infect_gauge=(#今日无症状仪表
        Gauge()
        .add(series_name="今日无症状", data_pair=[["今日无症状", int(today_no_infect_num)]],detail_label_opts=opts.LabelOpts(formatter="{value}人"))
        .set_global_opts(
            legend_opts=opts.LegendOpts(is_show=False),
            tooltip_opts=opts.TooltipOpts(is_show=False, formatter="{a} <br/>{b} : {c}人"),
        )
    )
    today_no_infect_gauge.chart_id='todaynoinfectgauge'
    return today_no_infect_gauge
#get_today_no_infect_gauge().render("today_no_infect_gauge.html")

while True:
    main_page=Page(layout=Page.DraggablePageLayout)
    main_page.add(
        get_total_confirm_map(),
        get_national_heal_rate_liquid(),
        get_national_death_rate_liquid(),
        get_today_confirm_gauge(),
        get_today_no_infect_gauge(),
    )
    main_page.render('main_page_temp.html')
    Page.save_resize_html('main_page_temp.html',cfg_file='./config_json/main_page.json',dest='./templates/main_page.html')
    now_page=Page(layout=Page.DraggablePageLayout)
    now_page.add(
        get_now_confirm_map(),
        get_now_confirm_pie()
    )
    now_page.render('now_page_temp.html')
    Page.save_resize_html('now_page_temp.html',cfg_file='./config_json/now_page.json',dest='./templates/now_page.html')
    heal_page=Page(layout=Page.DraggablePageLayout)
    heal_page.add(
        get_national_heal_rate_liquid(),
        get_total_heal_rate_bar()
    )
    heal_page.render('heal_page_temp.html')
    Page.save_resize_html('heal_page_temp.html',cfg_file='./config_json/heal_page.json',dest='./templates/heal_page.html')
    death_page=Page(layout=Page.DraggablePageLayout)
    death_page.add(
        get_national_death_rate_liquid(),
        get_total_death_rate_bar()
    )
    death_page.render('death_page_temp.html')
    Page.save_resize_html('death_page_temp.html',cfg_file='./config_json/death_page.json',dest='./templates/death_page.html')
    time.sleep(60)
#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  get_api.py
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
import requests
import json
def get_api_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#请求api函数，返回疫情数据字典
    response=requests.get(api_url)
    api_json=response.json()
    api_status_code=response.status_code
    if api_status_code!='200':
        api_data=json.loads(api_json['data'])
        return api_data
    else:
        return 0
def get_total_confirm_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省感染人数总计函数，返回字典
    original_dict=get_api_dict(api_url)
    total_confirm_dict={}
    total_confirm_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['confirm']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        total_confirm_dict[items['name']]=items['total']['confirm']
    return total_confirm_dict
def get_now_confirm_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省当前剩余感染人数函数，返回字典
    original_dict=get_api_dict(api_url)
    now_confirm_dict={}
    now_confirm_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['nowConfirm']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        now_confirm_dict[items['name']]=items['total']['nowConfirm']
    return now_confirm_dict
#print(get_now_confirm_dict())
def get_today_confirm_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省当日感染人数，返回字典
    original_dict=get_api_dict(api_url)
    today_confirm_dict={}
    today_confirm_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['today']['confirm']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        today_confirm_dict[items['name']]=items['today']['confirm']
    return today_confirm_dict
#print(get_today_confirm_dict())
def get_total_no_infect_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取全国无症状感染者总人数，返回值
    original_dict=get_api_dict(api_url)
    total_no_infect=original_dict['chinaTotal']['noInfect']#获取数据
    return total_no_infect
#print(get_total_no_infect_num())
def get_today_no_infect_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取全国今日无症状感染者人数，返回值
    original_dict=get_api_dict(api_url)
    today_no_infect=original_dict['chinaAdd']['noInfect']#获取数据
    return today_no_infect
#print(get_today_no_infect_num())
def get_today_death_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取全国今日死亡人数，返回值
    original_dict=get_api_dict(api_url)
    today_death=original_dict['chinaAdd']['dead']#获取全国数据
    return today_death
#print(get_today_death_num())
def get_total_death_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省死亡人数总计，返回字典
    original_dict=get_api_dict(api_url)
    total_death_dict={}
    total_death_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['dead']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        total_death_dict[items['name']]=items['total']['dead']
    return total_death_dict
#print(get_total_death_dict())
def get_heal_rate_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省治愈率统计，返回字典
    original_dict=get_api_dict(api_url)
    heal_rate_dict={}
    heal_rate_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['healRate']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        heal_rate_dict[items['name']]=items['total']['healRate']
    return heal_rate_dict
#print(get_heal_rate_dict())
def get_death_rate_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省死亡率统计，返回字典
    original_dict=get_api_dict(api_url)
    death_rate_dict={}
    death_rate_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['deadRate']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        death_rate_dict[items['name']]=items['total']['deadRate']
    return death_rate_dict
#print(get_death_rate_dict())
def get_today_heal_num(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取当日全国治愈人数，返回值
    original_dict=get_api_dict(api_url)
    today_heal=original_dict['chinaAdd']['heal']#获取全国数据
    return today_heal
#print(get_today_heal_num())
def get_total_heal_dict(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取分省治愈人数统计，返回字典
    original_dict=get_api_dict(api_url)
    total_heal_dict={}
    total_heal_dict[original_dict['areaTree'][0]['name']]=original_dict['areaTree'][0]['total']['heal']#获取全国数据
    for items in original_dict['areaTree'][0]['children']:#分省获取
        total_heal_dict[items['name']]=items['total']['heal']
    return total_heal_dict
#print(get_total_heal_dict())
def get_data_update_time(api_url='https://view.inews.qq.com/g2/getOnsInfo?name=disease_h5'):#获取数据更新时间，返回字符串
    original_dict=get_api_dict(api_url)
    data_update_time=original_dict['lastUpdateTime']
    return data_update_time
#print(get_data_update_time())

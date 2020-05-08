#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  flask_framework.py
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
from flask import Flask
from flask import render_template
app = Flask(__name__)
app.jinja_env.auto_reload = True
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def main_page():
    return render_template('main_page.html')

@app.route('/main_page/')
def main_page_back():
    return render_template('main_page.html')

@app.route('/now_page/')
def now_page():
    return render_template('now_page.html')

@app.route('/heal_page/')
def heal_page():
    return render_template('heal_page.html')

@app.route('/death_page/')
def death_page():
    return render_template('death_page.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port= 5000)#执行flask的运行

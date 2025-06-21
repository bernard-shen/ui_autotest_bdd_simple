#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import configparser
import os

configfile = configparser.ConfigParser()
curPath = os.path.abspath(os.path.dirname(__file__))
# 获取项目根路径，内容为当前项目的名字
rootPath = curPath[:curPath.find("automationtest\\") + len("automationtest\\")]
file = rootPath + 'config/sql_config.ini'
configfile.read(file, encoding='utf8')


def get_sql_config(module1,name):
    str1 = configfile[module1][name]
    new_sql = str1.lstrip('[').rstrip(']')
    sql_list = new_sql.split(',')
    return sql_list


if __name__ == '__main__':
    a = get_sql_config('mysql','AUTO-Mysql3-source')
    print(a)





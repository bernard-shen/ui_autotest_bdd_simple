#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import sys
import yaml
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(BASE_DIR)


def get_locations(page_name, module_name, locator_path=r'./config/dta/locations.yaml'):
    with open(locator_path, 'r', encoding='utf-8') as f:
        data_dict = yaml.safe_load(f.read())
    return data_dict[page_name][module_name]


if __name__ == '__main__':
    locations = get_locations("发现结果", '查询')
    print(type(locations))
    print(locations)
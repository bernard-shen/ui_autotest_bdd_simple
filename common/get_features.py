#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
import time
# from common.api_request import ReqClass
from common.get_location import get_locations
import requests
import os
import sys
from loguru import logger


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
root_dir = BASE_DIR.replace('common', '')
logger.add('{}logs/my_logs/用例组装_{}.txt'.format(root_dir, time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))
api_path = get_locations(page_name='自动化平台接口', module_name='基础接口', locator_path=r'{}config/common/api_url.yaml'.format(root_dir))
host = get_locations(page_name='自动化平台接口', module_name='公共部分', locator_path=r'{}config/common/api_url.yaml'.format(root_dir))

real_host = host["base_url"]
search_api = api_path["参数查询"]
base_url = real_host + search_api


class FeaturePrepare:
    def __init__(self, case_id):
        self.url = base_url
        self.body = {"caseId": case_id}
        self.res = requests.post(url=self.url, json=self.body)
        if self.res.status_code == 200:
            if json.loads(self.res.content)['code'] not in [0, 200]:
                logger.error('接口返回错误，响应码为：{code}，错误信息为：{msg}'.format(code=self.res.status_code, msg=json.loads(self.res.content)))
            else:
                self.response = json.loads(self.res.content)
        else:
            logger.error('接口返回错误，错误码为：{code}，错误信息为：{msg}'.format(code=self.res.status_code, msg=json.loads(self.res.content)))
        print(self.response)
        print('='*50)

    # 获取步骤顺序
    def get_order(self):
        list_order = []
        steps_dict = self.response['data']['nodeParam']
        for step in steps_dict:
            if step['nextNodeId'] is None:
                end = step['nodeId']
                list_order.insert(0, end)
                length = len(steps_dict)

                for i in range(length - 1):
                    for next_step in steps_dict:
                        if next_step["nextNodeId"] == end:
                            list_order.insert(0, next_step['nodeId'])
                            end = next_step['nodeId']
        if 'null' in list_order:
            list_order.remove('null')

        return list_order

    # 根据步骤顺序获取步骤参数
    def get_data(self):
        steps = []
        input_parameters = []
        output_parameters = []
        order = self.get_order()
        steps_dict = self.response['data']['nodeParam']
        for i in order:
            for data in steps_dict:
                if data['nodeId'] == i:
                    steps.append(data['nodeName']+('[{}]'.format(data['nodeCode'])))
                    input_parameters.append(data['inputMap'])
                    output_parameters.append(data['outputMap'])

        list_temp = [steps, input_parameters, output_parameters]
        return list_temp

    # 根据步骤顺序，拼装feature用例
    def new_feature(self):
        steps = self.get_data()[0]
        with open(r'{}test_cases/features/flow/隐私发现主流程.feature'.format(root_dir), 'w', encoding='utf8') as f:
            f.writelines('Feature: 隐私发现主流程测试\n')
            f.writelines('\n')
            f.writelines('  @流程测试-隐私发现主流程\n')
            f.writelines('  Scenario: 用例1:-隐私发现主流程-测试001\n')
            for i in range(len(steps)):
                f.write('    ' + 'Given ' + steps[i] + '\n')

    # 获取步骤输入--按node_code
    def get_step_input(self):
        data = self.get_data()
        code_id = [i.split('[')[1].split(']')[0] for i in data[0]]
        return dict(zip(code_id, data[1]))

    # 获取步骤输出--按node_code
    def get_step_output(self):
        data = self.get_data()
        new_id = [i.split('[')[1].split(']')[0] for i in data[0]]
        return dict(zip(new_id, data[2]))

    # 获取数据源信息
    def get_db_info(self):
        return self.response['data']['db']

    # 获取整个期望数据
    def get_expect_data(self):
        return json.loads(self.response['data']['expect'])

    # 获取步骤的node_id, 通过node_code
    def get_node_id(self):
        order = self.get_order()
        data = self.get_data()
        code_id = [i.split('[')[1].split(']')[0] for i in data[0]]
        return dict(zip(code_id, order))


if __name__ == '__main__':
    new_pre = FeaturePrepare(case_id=9823)
    new_pre.new_feature()




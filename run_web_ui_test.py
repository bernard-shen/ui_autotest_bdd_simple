#!/usr/bin/python
# -*- coding: UTF-8 -*-
from base.web_ui_conf_reader import WebUIConfReader
from common.date_time_tool import DateTimeTool
from init.web_ui_init import web_ui_init
import argparse
import pytest
import os
from common.get_features import FeaturePrepare
import sys
from loguru import logger


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-k', '--keyword', help='只执行匹配关键字的用例，会匹配文件名', type=str)
    parser.add_argument('-d', '--dir', help='指定要测试的目录', type=str)
    parser.add_argument('-m', '--markexpr', help='只运行符合给定的mark表达式的测试', type=str)
    parser.add_argument('-s', '--capture', help='是否在标准输出流中输出日志,1:是、0:否,默认为0', type=str)
    parser.add_argument('-r', '--reruns', help='失败重跑次数,默认为0', type=str)
    parser.add_argument('-lf', '--lf', help='是否运行上一次失败的用例,1:是、0:否,默认为0', type=str)
    parser.add_argument('-clr', '--clr', help='是否清空已有测试结果,1:是、0:否,默认为0', type=str)
    parser.add_argument('-n', '--n', help='n是指定并发数', type=str)
    parser.add_argument('-task_id', '--task_id', help='task_id-任务编号', type=str)
    parser.add_argument('-case_id', '--case_id', help='case_id-用例编号', type=str)
    args = parser.parse_args()

    print('%s初始化基础数据......' % DateTimeTool.get_now_time())
    web_ui_init()
    print('%s初始化基础数据完成......' % DateTimeTool.get_now_time())
    print('%s初始化完成......' % DateTimeTool.get_now_time())

    print('%s开始测试......' % DateTimeTool.get_now_time())
    exit_code = 0
    web_ui_config = WebUIConfReader().config
    for current_browser in web_ui_config.test_browsers:
        print('%s开始%s浏览器测试......' % (DateTimeTool.get_now_time(), current_browser))
        # 执行pytest前的参数准备
        pytest_execute_params = ['-c', 'config/pytest.ini', '-v']
        # 是否无头模式
        if web_ui_config.is_headed == 'true':
            # pass
            pytest_execute_params.append('--headed')
            pytest_execute_params.append('--slowmo')
            pytest_execute_params.append('200')

        if args.keyword:
            pytest_execute_params.append('-k')
            pytest_execute_params.append(args.keyword)

        if args.n:
            pytest_execute_params.append('-n')
            pytest_execute_params.append(args.n)
        if args.markexpr:
            pytest_execute_params.append('-m')
            pytest_execute_params.append(args.markexpr)
        # 判断是否输出日志
        if args.capture:
            if int(args.capture):
                pytest_execute_params.append('-s')
        # 判断是否失败重跑
        if args.reruns:
            if int(args.reruns):
                pytest_execute_params.append('--reruns')
                pytest_execute_params.append(args.reruns)
        # 判断是否只运行上一次失败的用例
        if args.lf:
            if int(args.lf):
                pytest_execute_params.append('--lf')
        # 判断是否清空已有测试结果
        if args.clr:
            if int(args.clr):
                pytest_execute_params.append('--clean-alluredir')
        # 设置测试用例目录
        # 判断目录参数
        case_dir = 'test_cases/web_ui/'
        if args.dir:
            case_dir = args.dir
        pytest_execute_params.append(case_dir)

        tmp_exit_code = pytest.main(pytest_execute_params)
        if not tmp_exit_code == 0:
            exit_code = tmp_exit_code
        print('%s结束%s浏览器测试......' % (DateTimeTool.get_now_time(), current_browser))

    print('%s结束测试......' % DateTimeTool.get_now_time())

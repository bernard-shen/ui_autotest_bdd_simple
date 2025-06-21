#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

import os
import os.path


class Rename:
    @staticmethod
    def change_dir(tar_dir):
        dir_path = os.getcwd()
        print(dir_path)
        if r'test_cases\web_ui' not in dir_path:
            os.chdir('../test_cases/web_ui/{}'.format(tar_dir))
        else:
            os.chdir('../{}'.format(tar_dir))

    @staticmethod
    def get_files(dir_path):
        return os.listdir(dir_path)

    @staticmethod
    def rename_file(old_file, mode=None, char=None):
        if old_file not in ['__init__.py', 'conftest.py']:
            if mode:
                if mode == '+':
                    if char:
                        os.rename(file_name, char + file_name)
                    else:
                        if 'a' != old_file[0]:
                            os.rename(old_file, 'a' + old_file)
                elif mode == '-':
                    if 'a' == old_file[0]:
                        os.rename(old_file, old_file[1:])
            else:
                if char:
                    os.rename(file_name, char + file_name)
                else:
                    if 'a' != old_file[0]:
                        os.rename(old_file, 'a'+old_file)
        return True


if __name__ == '__main__':
    choice = str(input("please input the choice between '+' and '-':\n"))
    while choice not in ['+', '-']:
        choice = str(input("please input the choice between '+' and '-':\n"))

    new_rename = Rename()
    dir_list = ['common', 'dta', 'dte', 'dtk', 'dtm']
    for dd in dir_list:
        new_rename.change_dir(tar_dir=dd)
        file_list = new_rename.get_files(dir_path=os.getcwd())
        # file_list_mine = ['test_find_history_single.py', 'test_find_result_single.py',  'test_masking_plan_config.py', 'test_mask_algorithm.py', 'test_secret_plan_config.py', 'test_secret_type.py', 'test_connect_single.py', 'test_masking_task_single.py', 'test_risk_analysis.py', 'test_encryption_task_info.py']
        # file_list_mine_a = ['atest_find_history_single.py', 'atest_find_result_single.py',  'atest_masking_plan_config.py', 'atest_mask_algorithm.py', 'atest_secret_plan_config.py', 'atest_secret_type.py', 'test_connect_single.py', 'atest_masking_task_single.py', 'atest_risk_analysis.py', 'atest_encryption_task_info.py']
        for ff in file_list:
            if choice == '+':
                new_rename.rename_file(old_file=ff)
            else:
                new_rename.rename_file(old_file=ff, mode='-')
                print("文件{}名称更改成功。。。".format(ff))

        new_rename.change_dir(tar_dir='../')


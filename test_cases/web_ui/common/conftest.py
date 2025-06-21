# from test_cases.web_ui.dta.test_masking_task_single import *
# from test_cases.web_ui.common.test_secret_plan_config import *
# from test_cases.web_ui.common.test_secret_type import *
# from test_cases.web_ui.common.test_mask_algorithm import *
# from test_cases.web_ui.dta.test_risk_analysis import *
# from test_cases.web_ui.dtk.atest_key_manage_system import *
# from test_cases.web_ui.dta.atest_access_manage_safety_rule import *
# from test_cases.web_ui.dta.atest_access_manage_access_group import *
# from test_cases.web_ui.dta.atest_access_manage_safety_plan import *
# from test_cases.web_ui.dta.atest_access_group_user_auth import *
# from test_cases.web_ui.dte.atest_encryption_plan import *
# from test_cases.web_ui.dta.atest_connect_single import *

import pytest
import time
import random
from base.dta.web_ui_dta_conf_reader import WebUIDtaConfReader
from base.dta.web_ui_dta_data_reader import WebUIDtaDataReader
from pages.common.login_page import LoginPage



@pytest.fixture(scope='session')
def pages():
    return WebUIDtaConfReader().config.pages

# @pytest.fixture(scope='session')
# def user():
#     return WebUIDtaDataReader().data['user']

# @pytest.fixture(autouse=True)
# def login(page, pages, user):
#     LoginPage(pages['login_page'], page).login(user['username'], user['password'])
#     time.sleep(0.2)


@pytest.fixture(scope='session')
def user():
    user_list = []
    num = len(WebUIDtaDataReader().data)
    for i in range(1, int(num)+1):
        user_info = WebUIDtaDataReader().data['user'+str(i)]
        user_list.append(user_info["username"])
    return user_list


@pytest.fixture(autouse=True)
def login(page, pages, user):
    t_time = float(str(random.random())[:4])
    time.sleep(t_time)
    user_name = random.choice(user)
    passwd = WebUIDtaDataReader().data['user1']["password"]
    LoginPage(pages['login_page'], page).login(user_name, passwd)
    time.sleep(0.2)


# def pytest_configure(config):
#     marker_list = ["脱敏任务", "访问分组", "分组管理", "DTA", "安全方案"]  # 标签名集合
#     for markers in marker_list:
#         config.addinivalue_line("markers", markers)





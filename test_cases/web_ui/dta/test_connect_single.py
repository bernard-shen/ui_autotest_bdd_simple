import allure
import pytest
from common.data_table import data_table
from playwright.sync_api import expect
from playwright.sync_api import Page, expect
from pytest_bdd import scenario,scenarios, given, when, then, parsers
from loguru import logger
import time
from pages.common.connection_page import ConnectionPage
from common.get_location import get_locations
# from pages.common.secret_find_page import FindResult


locations_new = get_locations(page_name='数据连接', module_name='新建连接部分')
locations_search = get_locations(page_name='数据连接', module_name='查询部分')
locations_list = get_locations(page_name='数据连接', module_name='列表部分')
locations_detail = get_locations(page_name='数据连接', module_name='详情页部分')
locations_detail1 = get_locations(page_name='数据连接', module_name='详情页-任务信息')

scenarios('./dta/自动化用例-数据连接-单模块.feature')
logger.add('../logs/mylogs/{}.txt'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))


def make_screenshot(page, case_order):
    time_stamp = str(time.time() * 1000).split('.')[0]
    allure.attach(page.screenshot(path='./test_data/screen_shots/用例{}_{}.png'.format(str(case_order), time_stamp)),
                  '页面截图_用例{}_{}'.format(str(case_order), time_stamp), allure.attachment_type.PNG)


@given('已登录到DTA环境 "http://192.168.9.116"')
def step_impl():
    time.sleep(1)


@given("已成功进入数据连接页面")
@allure.severity(allure.severity_level.CRITICAL)
def step_impl(page, pages):
    page.goto(pages['connection_page'])
    time.sleep(1)


@given('页面左上角包含"新建连接"按钮')
def step_impl(page):
    expect(page.locator(locations_new['新建连接'])).to_be_visible()


# Scenario: 1.验证"新建连接"按钮能否点击
@when('点击"新建连接"')
@allure.story("新建数据连接")
def step_impl(page):
    with allure.step("点击新建连接"):
        page.locator(locations_new['新建连接']).highlight()
        time.sleep(2)
        page.locator(locations_new['新建连接']).click()
    time.sleep(2)


@then("进入新建连接页面")
def step_impl(page, pages):
    url = page.url
    assert 'connection/manage' in url


# Scenario: 2.验证新建连接页面布局是否正确
@allure.feature("ip检查")
@given("已进入新建连接页面")
@allure.feature("ip检查")
def step_impl(page, pages):
    page.goto(pages['connection_manage_page'])
    time.sleep(1)


@when('点击"高级选项"')
def step_impl(page):
    page.locator("//h2[text()='高级选项 ']").click()
    time.sleep(0.2)


@then('展开参数"是否为加密库"、"自定义参数"')
def step_impl(page):
    locs = ["//label[text()='是否为加密库：']", "//label[text()='自定义参数：']"]
    for i in locs:
        expect(page.locator(i)).to_be_visible()


@then('页面包含字段:"连接名称"、"数据源类型"、"子机构可用"、"IP地址"、"端口"、"连接模式"、"数据库名称"、"认证方式"、"用户名"、"密码"')
def step_impl(page):
    list_loc = ["连接名称：", "数据源类型：", "子机构可用：", "IP地址：", "端口：", "连接模式：", "数据库名称：", "认证方式：", "用户名：", "密码："]
    loc_normal = "//label[text()='{}']"
    for i in list_loc:
        expect(page.locator(loc_normal.format(i))).to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/page_columns.png'), '页面字段展示', allure.attachment_type.PNG)


@then('包含"测试连接"、"保存为草稿"、"保存"、"返回"按钮')
def step_impl(page):
    locs_new = [locations_new["测试连接"], locations_new["保存为草稿"], locations_new["保存"], locations_new["返回"]]
    for i in locs_new:
        expect(page.locator(i)).to_be_visible()


# Scenario: 3.验证新建连接页面IP地址能否为空
@given(parsers.cfparse("已填写任意连接名称[{conn_name1}]"))
@allure.title("ip检查22")
def step_impl(page, conn_name1):
    page.locator(locations_new['连接名称']).fill(conn_name1)


@when("IP地址内容输入为空")
def step_impl(page):
    page.locator(locations_new['ip地址']).fill('')
    time.sleep(1)


@when("鼠标与输入框失去焦点时")
def step_impl(page):
    loc1 = "//h2[text()='连接信息']"
    page.locator(loc1).click()
    time.sleep(0.5)


@when('点击"保存"')
def step_impl(page):
    time.sleep(1.2)
    page.locator(locations_new['保存']).click()
    time.sleep(1.2)


@when('点击"保存"连接')
def step_impl(page):
    page.locator(locations_new['保存']).click()
    time.sleep(20)


@then(parsers.cfparse("IP地址输入框下方出现提示:[{content}]"))
def step_impl(page, content):
    error_loc = "//label[@for='host']/following-sibling::div//div[@class='el-form-item__error']"
    page.locator(error_loc).highlight()
    # content = page.locator(error_loc).text_content()
    expect(page.locator(error_loc)).to_contain_text(content)
    allure.attach(page.screenshot(path='./test_data/screen_shots/ip_info.png'), 'ip输入提示', allure.attachment_type.PNG)


# Scenario Outline: 4.验证新建连接页面连接名称输入非法内容  进入脱敏任务页面
@when(parsers.parse("输入连接名称1为{connect_name}"))
def step_impl(page, connect_name):
    page.locator(locations_new['连接名称']).fill(connect_name)
    page.locator(locations_new['连接名称']).press('Tab')


@then(parsers.cfparse('连接名称输入框下方出现提示:[{msg}]'))
def step_impl(page, msg):
    time.sleep(0.2)
    error_loc = "//label[@for='aliasName']/following-sibling::div//div[@class='el-form-item__error']"
    content = page.locator(error_loc).text_content()
    assert msg in content


# Scenario: 5.验证新建连接页面连接名称输入超过30个字符
@then('下方出现提示:"最多输入30个字符"')
def step_impl(page):
    error_loc = "//label[@for='aliasName']/following-sibling::div//div[@class='el-form-item__error']"
    expect(page.locator(error_loc)).to_contain_text('最多输入30个字符')
    allure.attach(page.screenshot(path='./test_data/screen_shots/info001.png'), '连接名输入框提示', allure.attachment_type.PNG)


@when(parsers.cfparse("输入连接名称2为[{conn_name}]"))
def step_impl(page, conn_name):
    page.locator(locations_new['连接名称']).fill(conn_name)


# Scenario: 6.验证新建连接页面连接名称能否为空
@when("输入连接名称为空")
def step_impl(page):
    page.locator(locations_new['连接名称']).fill('')


# Scenario: 7.验证新建连接页面查看数据源类型是否匹配
@when("点击数据源类型下拉单选框")
def step_impl(page):
    page.locator(locations_new['数据源类型']).click()


@then(data_table("包含下方数据源可选", fixture="data_source"))
def step_impl(page, data_source):
    for i in range(len(data_source)):
        if data_source[i]["db_source"] == "XHHive":
            expect(page.locator("li:has-text('XHHive') >> nth=0")).to_be_visible()
        elif data_source[i]["db_source"] == "Hive":
            expect(page.locator("//li/span[text()='Hive']")).to_be_visible()
        else:
            # expect(page.locator("li:has-text('{}')".format(data_source[i]["db_source"]))).to_be_visible()
            expect(page.locator("//li/span[text()='{}']".format(data_source[i]["db_source"]))).to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/info007.png'), '数据源可选', allure.attachment_type.PNG)


# Scenario: 8.验证新建连接页面IP地址输入非法的IP地址
@when(parsers.parse("输入下方的IP地址{ip}"))
def step_impl(page, ip):
    page.locator(locations_new['ip地址']).fill(ip)


# Scenario Outline: 9.验证新建连接页面-自动测试连接失败修改后再次点击测试连接成功
@given(parsers.parse("选择数据源{db_source},连接参数输入{connect_name}、{ip}、{port}、{db_name}、{username}、{password}"))
def step_impl(page, db_source, connect_name, ip, port, db_name, username, password):
    page.locator(locations_new["数据源类型"]).click()
    if db_source == "XHHive":
        page.locator("li:has-text('XHHive') >> nth=0").click()
    elif db_source == "Hive":
        page.locator("//li/span[text()='Hive']").click()
    elif db_source == "Mysql":
        page.locator("//li/span[text()='Mysql']").click()
    elif db_source == "Oracle":
        page.locator("//li/span[text()='Oracle']").click()
    else:
        page.locator("li:has-text('{}')".format(db_source)).click()

    if db_source != "Mysql":
        page.locator(locations_new['连接名称']).fill(connect_name)
        page.locator(locations_new['ip地址']).fill(ip)
        page.locator(locations_new['端口']).fill(port)
        page.locator(locations_new['数据库名称']).fill(db_name)
        page.locator(locations_new['用户名']).fill(username)
        page.locator(locations_new['密码']).fill(password)
    else:
        page.locator(locations_new['连接名称']).fill(connect_name)
        page.locator(locations_new['ip地址']).fill(ip)
        page.locator(locations_new['端口']).fill(port)
        page.locator(locations_new['用户名']).fill(username)
        page.locator(locations_new['密码']).fill(password)


@when("点击测试连接")
def step_impl(page):
    time.sleep(1)
    make_screenshot(page, case_order=11)
    page.locator(locations_new['测试连接']).highlight()
    page.locator(locations_new['测试连接']).dblclick()
    time.sleep(0.1)


@then('系统提示:"连接失败"')
def step_impl(page):
    time.sleep(15)
    loc_info = "//div[@role='alert']//p"
    page.wait_for_selector(loc_info)
    make_screenshot(page, case_order=9)
    loc = "//div[@role='alert']//p[text()='连接失败']"
    page.wait_for_selector(loc, timeout=45000)
    expect(page.locator(loc)).to_be_visible()
    make_screenshot(page, case_order=9)
    time.sleep(2)


@then('系统提示:"连接失败1"')
def step_impl(page):
    time.sleep(5)
    loc_info = "//div[@role='alert']//p"
    loc1 = "//div[@role='alert']//p[text()='连接失败']"
    loc2 = "//div[@role='alert']//p[text()='连接成功']"
    for i in range(1200):
        if page.locator(loc1).is_visible():
            make_screenshot(page, 111)
            break
        elif page.locator(loc2).is_visible():
            make_screenshot(page, 222)
            break
        elif page.locator(loc_info).is_visible():
            make_screenshot(page, 333)
            break
        else:
            time.sleep(0.1)
            logger.info('第{}次'.format(str(i)))

    expect(page.locator(loc1)).to_be_visible()
    time.sleep(2)


@when(parsers.cfparse("修改password为[{password}]"))
def step_impl(page, password):
    page.locator(locations_new['密码']).fill(password)


@then('系统提示:"连接成功"')
def step_impl(page):
    page.wait_for_selector("//div[@role='alert']//p", timeout=30000)
    if page.locator("//div[@role='alert']//p[text()='连接成功']").is_visible():
        make_screenshot(page, case_order=11)
    elif page.locator("//div[@role='alert']//p[text()='连接失败']").is_visible():
        make_screenshot(page, case_order=11)
        raise
    else:
        make_screenshot(page, case_order=11)
        raise


# 10.验证新建连接页面-自动测试连接失败再次点击测试连接失败
@when(parsers.parse("1选择数据源{db_source},连接参数输入{connect_name}、{ip}、{port}、{db_name}、{username}、{password}"))
def step_impl(page, pages, db_source, connect_name, ip, port, db_name, username, password):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.choice_sql_type(db_source)
    data_list = [connect_name, ip, port, username, password, db_name]
    new_conn.fill_connection(sql_type=db_source, data_type='list', data_values=data_list)


@then('页面下方显示"隐私发现任务参数"部分')
def step_impl(page):
    page.wait_for_selector("//h3[text()='隐私发现任务参数']")
    expect(page.locator("//h3[text()='隐私发现任务参数']")).to_be_visible()
    make_screenshot(page, case_order=11)

#  Scenario Outline: 11.验证新建连接页面-自动测试连接成功
# pass
# Scenario Outline: 12.验证新建连接页面-自动测试连接失败保存能否保存为异常连接


@then(parsers.cfparse('页面弹出提示框[{msg}]'))
def step_impl(page, msg):
    time.sleep(5)
    loc_info = "//div[@role='alert']//p"
    page.wait_for_selector(loc_info)
    make_screenshot(page, case_order=9)

    loc = "div[role='alert']:has-text('{}')".format(msg)
    page.wait_for_selector(loc,timeout=30000)
    page.locator(loc).click()
    expect(page.locator(loc)).to_be_visible()


@then(parsers.cfparse('页面弹出1提示框[{msg}]'))
def step_impl(page, msg):
    time.sleep(5)
    loc = "div[role='alert']:has-text('{}')".format(msg)
    for i in range(1200):
        if page.locator(loc).is_visible():
            make_screenshot(page, 333)
            break
        elif page.locator("div[role='alert']:has-text('网络超时')").is_visible():
            make_screenshot(page, 333)
            break
        else:
            time.sleep(0.1)
            logger.info('第{}次'.format(str(i)))
    expect(page.locator(loc)).to_be_visible()
    time.sleep(1)


@then(parsers.parse('列表新增一条连接名称为{connect_name},连接状态为"异常"的数据'), target_fixture="secret_status")
def step_impl(page, pages, connect_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(connect_name)
    time.sleep(0.5)
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == '异常'
    secret_status = page.locator(locations_list["隐私识别状态-无内容"]).text_content().split(' ')[-1]
    return secret_status


@then('该连接隐私识别状态为"-"')
def step_impl(page, secret_status):
    assert secret_status == '-'


# Scenario: 13.验证新建连接页面-取消新增能否成功
@when(data_table("依次输入conn_name、ip、port、db_name、user、password", fixture="conn_data"))
def step_impl(page, pages, conn_data):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.fill_connection(sql_type="Oracle", data_values=conn_data[0])


@when("点击返回")
def step_impl(page):
    page.locator(locations_new["返回"]).click()


@then(parsers.cfparse("数据连接列表页,搜索[{conn_name}],连接不存在"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    time.sleep(0.5)
    num = new_conn.get_num()
    assert num == 0


# Scenario Outline: 14.验证新增数据连接-发现全部数据,能否新建成功
# Scenario Outline: 15.验证新增数据连接-发现部分数据,能否新建成功
@when(parsers.parse('发现范围选择"发现部分",勾选{find_schema}'))
def step_impl(page, pages, find_schema):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.part_data_db(find_schema)


@then("新建连接成功,触发隐私发现")
def step_impl(page):
    loc = "div[role='alert']:has-text('保存成功，已开启隐私发现')"
    page.locator(loc).click()
    expect(page.locator(loc)).to_be_visible()


# Scenario: 16.验证新建连接页面用户名能否为空
@when("用户名输入为空")
def step_impl():
    pass


@then(parsers.cfparse("用户名输入框下方出现提示:[{content}]"))
def step_impl(page, content):
    error_loc = "//label[@for='userName']/following-sibling::div//div[@class='el-form-item__error']"
    # content = page.locator(error_loc).text_content()
    expect(page.locator(error_loc)).to_contain_text(content)


# Scenario Outline: 17.验证新增数据连接-保存草稿能否成功


@when("点击保存草稿")
def step_impl(page):
    page.locator(locations_new["保存为草稿"]).click()


@then('系统提示:"保存草稿成功"')
def step_impl(page):
    loc = "div[role='alert']:has-text('已成功保存为草稿！')"
    page.locator(loc).click()
    expect(page.locator(loc)).to_be_visible()


@then(parsers.parse('列表新增一条连接名称为{connect_name}，数据源状态为"草稿"的数据'))
def step_impl(page, pages, connect_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(connect_name)
    time.sleep(0.5)
    connect_status = page.locator(locations_list["数据源状态"]).text_content().strip(' ')
    assert connect_status == '草稿'


# 18
@when(parsers.cfparse("输入已存在的连接名称[{conn_name}]"))
def step_impl(page, conn_name):
    page.locator(locations_new['连接名称']).fill(conn_name)


# Scenario: 19.验证新建连接页面-数据源类型为Oracle,输入不合法的数据库名称
@when('数据源库类型选择"Oracle"')
def step_impl():
    pass
# 默认


@when(parsers.parse("数据库名称输入[{db_name}]"))
def step_impl(page, db_name):
    page.locator(locations_new["数据库名称"]).fill(db_name)


@then(parsers.parse('数据库名称输入框下方出现提示:[{msg}]'))
def step_impl(page, msg):
    error_loc = "//label[@for='dbName']/following-sibling::div//div[@class='el-form-item__error']"
    content = page.locator(error_loc).text_content()
    assert msg in content


# Scenario: 20.验证新建连接页面-数据库名称能否为空
@when("数据库名称输入为空")
def step_impl(page):
    page.locator(locations_new["数据库名称"]).fill('')


# # #
@when(parsers.parse("数据连接名称{connect_name}非空"))
def step_impl(page, connect_name):
    pass


@then(parsers.parse("数据连接名称{connect_name}非空时，删除连接成功"))
def step_impl(page, pages, connect_name):
    time.sleep(1)
    page.goto(pages['connection_page'])
    if connect_name == "null":
        pass
    else:
        new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
        new_conn.search_connection(connection_name='SHEN')
        time.sleep(1)
        num = new_conn.get_num()
        for i in range(num):
            new_conn.search_connection(connection_name='SHEN')
            new_conn.del_connection(connection_name='SHEN')
            time.sleep(0.5)



@then("删除此连接")
def step_impl(page, pages):
    time.sleep(1)
    page.goto(pages['connection_page'])
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    num = page.locator("//span[@class='el-pagination__total']").text_content().split(' ')[1]
    for i in range(1, int(num)+1):
        new_conn.del_connection(i)
        page.reload()


# 21.验证复制连接能否点击
@when(parsers.cfparse('选择已存在的连接[{conn_name}],点击"复制"'))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    time.sleep(1)
    page.locator(locations_list["复制按钮"]).click()


@then("进入复制连接页面")
def step_impl(page):
    expect(page.locator("//h1[text()='复制连接']")).to_be_visible()


# Scenario: 22.验证复制连接页面-连接名称是否不能重复
@given(parsers.cfparse('存在连接名称为[{conn_name}]的数据连接'),target_fixture="conn_name")
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    time.sleep(1)
    num = new_conn.get_num()
    assert num == 1
    return conn_name


@given(data_table('页面存在发现部分数据源的数据连接A,不存在则新建', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    time.sleep(1)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(sql_type=data_list[0]["db_source"], dbname=data_list[0]["find_schema"], data_values=data_list[0])
    time.sleep(2)
    new_conn.search_connection(conn_name)
    return conn_name


@given("已进入该连接的复制页面")
def step_impl(page):
    page.locator(locations_list["复制按钮"]).click()
    time.sleep(5)
    make_screenshot(page, case_order=25)


@when(parsers.cfparse('连接名称输入已存在的连接名称[{conn_name}]'))
def step_impl(page, conn_name):
    page.locator(locations_new['连接名称']).fill(conn_name)


@when('连接名称输入存在的连接名称A')
def step_impl(page, conn_name):
    page.locator(locations_new['连接名称']).fill(conn_name)
    time.sleep(0.5)


# Scenario: 23.验证复制连接页面-连接名称能否为空
@when("连接名称输入为空")
def step_impl(page):
    page.locator(locations_new['连接名称']).fill("")


# Scenario Outline: 25.验证复制连接-选择发现全部数据-是否成功
@given(parsers.parse("列表存在数据连接{conn_name}，不存在则使用{db_source},{ip},{port},{username},{password},{db_name}新建"))
def step_impl(page, pages, conn_name, db_source, ip, port, username, password, db_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    value_list = [conn_name, ip, port, username, password, db_name]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(sql_type=db_source, data_values=value_list, data_type='list')
    time.sleep(1.5)
    new_conn.search_connection(conn_name)
    time.sleep(1)


@given(parsers.parse("已经存在数据连接{conn_name}，不存在则使用{db_source},{ip},{port},{username},{password},{db_name},{find_schema}新建"))
def step_impl(page, pages, conn_name, db_source, ip, port, username, password, db_name, find_schema):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    value_list = [conn_name, ip, port, username, password, db_name]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(sql_type=db_source, data_values=value_list, data_type='list', dbname=find_schema)
    time.sleep(1.5)
    new_conn.search_connection(conn_name)
    time.sleep(1)


@when(parsers.parse("连接名称填入{conn_name1},用户名填入{username},密码填入{password}"))
def step_impl(page, pages, conn_name1, username, password):
    page.locator(locations_new['连接名称']).fill(conn_name1)
    if 'presto' in conn_name1.lower():
        page.locator(locations_new['用户名']).fill(username)
    elif 'clickhouse' in conn_name1.lower():
        pass
    else:
        page.locator(locations_new['用户名']).fill(username)
        page.locator(locations_new['密码']).fill(password)


@when('点击"连接信息"')
def step_impl(page):
    loc1 = "//h2[text()='连接信息']"
    page.locator(loc1).click()


@when('再次点击"保存"')
def step_impl(page):
    page.locator(locations_new['保存']).click()


@then(parsers.parse("保存成功,回到数据连接页面,页面新增一条{conn_name1}的数据连接"))
def step_impl(page, pages, conn_name1):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name1)
    num = new_conn.get_num()
    assert num == 1


# 26.验证复制连接-选择发现部分数据-是否成功
@when(parsers.parse("选择发现范围{find_schema}"))
def step_impl(page, pages, find_schema):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.part_data_db(find_schema)


# Scenario Outline: 27.验证复制连接-保存草稿能否成功

@when(parsers.parse("仅填入连接名称{conn_name1}"))
def step_impl(page, conn_name1):
    time.sleep(0.2)
    page.locator(locations_new['连接名称']).fill(conn_name1)
    time.sleep(0.5)


@when('点击"保存为草稿"')
def step_impl(page):
    page.locator(locations_new['保存为草稿']).click()
    time.sleep(2)


@then(parsers.parse("列表新增一条名称为{conn_name1}的数据连接"),target_fixture="connect_status")
def step_impl(page, pages, conn_name1):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name1)
    num = new_conn.get_num()
    assert num == 1
    connect_status = page.locator(locations_list["数据源状态"]).text_content().strip(' ')
    return connect_status

@then("该连接数据源状态为[草稿]")
def step_impl(connect_status):
    assert connect_status == '草稿'


# Scenario: 28.验证复制连接页面-测试连接失败能否保存为异常连接
@then(parsers.cfparse('连接页面新增一条数据源状态为"异常"的数据连接[{conn_name}]'))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    assert num == 1


@when(parsers.cfparse("输入具体的连接名[{conn_name}],用户名[{username}],密码[{password}]"))
def step_impl(page, pages, conn_name, username, password):
    page.locator(locations_new['连接名称']).fill(conn_name)
    page.locator(locations_new['用户名']).fill(username)
    page.locator(locations_new['密码']).fill(password)


@then(parsers.cfparse('搜索和删除对应数据连接[{conn_name}]成功'))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 1:
        new_conn.del_connection(conn_name)


@then(parsers.parse('搜索、删除对应数据连接{conn_name_copy1}成功'))
def step_impl(page, pages, conn_name_copy1):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name_copy1)
    time.sleep(3)
    num = new_conn.get_num()
    if num == 1:
        new_conn.del_connection(conn_name_copy1)


# Scenario: 29.验证复制连接页面-密码能否为空
@when(parsers.parse("连接名称输入任意非重复名称[{conn_name}],用户名输入[{username}],密码输入为空"))
def step_impl(page, pages, conn_name, username):
    page.locator(locations_new['连接名称']).fill(conn_name)
    page.locator(locations_new['用户名']).fill(username)
    page.locator(locations_new['密码']).fill('')


# Scenario: 30.验证复制连接页面-用户名能否为空
@when(parsers.parse("连接名称输入任意非重复名称[{conn_name}],用户名输入为空"))
def step_impl(page, conn_name):
    page.locator(locations_new['连接名称']).fill(conn_name)
    page.locator(locations_new['用户名']).fill('')


# Scenario: 31.验证复制连接页面-修改连接参数,是否可以复制成功
@when(parsers.parse("连接名称输入任意非重复名称[{conn_name}],修改ip为[{ip}],用户名输入[{username}],密码输入[{password}],端口输入[{port}]"))
def step_impl(page, conn_name, ip, username, password, port):
    page.locator(locations_new['连接名称']).fill(conn_name)
    page.locator(locations_new['ip地址']).fill(ip)
    page.locator(locations_new['用户名']).fill(username)
    page.locator(locations_new['密码']).fill(password)
    page.locator(locations_new['端口']).fill(port)


@then("保存成功")
def step_impl(page):
    loc = "div[role='alert']:has-text('保存成功，已开启隐私发现')"
    page.locator(loc).click()
    expect(page.locator(loc)).to_be_visible()


@then(parsers.cfparse("页面新增一条名称为[{conn_name}]的数据源"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    assert num == 1


# Scenario: 32.验证复制连接页面-数据库名称能否为空
@when(parsers.cfparse("连接名称输入任意非重复名称[{conn_name}],修改数据库名称为空,用户名输入[{username}],密码输入[{password}]"))
def step_impl(page, conn_name, username, password):
    page.locator(locations_new['连接名称']).fill(conn_name)
    page.locator(locations_new['用户名']).fill(username)
    page.locator(locations_new['密码']).fill(password)
    page.locator(locations_new['数据库名称']).fill("")


# Scenario: 33.验证复制连接-取消复制能否成功
@then(parsers.cfparse("回到数据连接列表页面,搜索[{conn_name}]，仅有一条"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    assert num == 1


# Scenario Outline: 34.验证新建连接-分别创建不同版本,不同编码,不同实例的Oracle数据连接,是否可以创建成功
@then(parsers.parse("新建连接成功,触发隐私发现,{conn_name}连接状态正常"))
def step_impl(page, pages, conn_name):
    loc = "div[role='alert']:has-text('保存成功，已开启隐私发现')"
    page.locator(loc).click()
    expect(page.locator(loc)).to_be_visible()
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == '正常'


# Scenario: 38.验证修改连接-点击修改,是否进入修改连接页面
@when('点击"修改"')
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    page.locator(locations_list["修改按钮"]).click()


@then("进入该连接的修改连接页面")
def step_impl(page):
    expect(page.locator("//h1[text()='修改连接']")).to_be_visible()


@then('页面包含字段:"连接名称"、"数据源类型"、"子机构可用"、"IP地址"、"端口"、"认证方式"、"用户名"、"密码"')
def step_impl(page):
    list_loc = ["连接名称：", "数据源类型：", "子机构可用：", "IP地址：", "端口：", "认证方式：", "用户名：", "密码："]
    loc_normal = "//label[text()='{}']"
    for i in list_loc:
        expect(page.locator(loc_normal.format(i))).to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/page_columns.png'), '页面字段展示', allure.attachment_type.PNG)


# def teardown_module(page, pages):
#     time.sleep(1)
#     page.goto(pages['connection_page'])
#     list_connections1 = ['AUTO-Oracle1', 'AUTO-Mysql1', 'AUTO-Postgresql1', 'AUTO-DB21', 'AUTO-Hive', 'AUTO-XHHiev1', 'AUTO-Gbase1', 'AUTO-Presto1', 'AUTO-ClickHouse1', 'AUTO-Oracle3', 'AUTO-Mysql3', 'AUTO-Postgresql3', 'AUTO-DB23', 'AUTO-Hive3', 'AUTO-XHHiev3', 'AUTO-Gbase3', 'AUTO-Presto3', 'AUTO-ClickHouse3', 'AUTO-Oracle4', 'AUTO-Mysql4', 'AUTO-Postgresql4', 'AUTO-DB24', 'AUTO-Hive4', 'AUTO-XHHiev4', 'AUTO-Gbase4', 'AUTO-Presto4', 'AUTO-ClickHouse4']
#     list_connections2 = ['AUTO-Oracle5','AUTO-Mysql5','AUTO-Postgresql5','AUTO-DB25','AUTO-HIVE5','AUTO-XHHive5','AUTO-Gbase5','AUTO-Presto5','AUTO-ClickHouse5','AUTO-Oracle6','AUTO-Mysql6','AUTO-Postgresql6','AUTO-DB26','AUTO-HIVE6','AUTO-XHHive6','AUTO-Gbase6','AUTO-Presto6','AUTO-ClickHouse6','CG-Oracle6','CG-Mysql6','CG-Postgresql6','CG-DB26','CG-HIVE6','CG-XHHive6','CG-Gbase6','CG-Presto6','CG-ClickHouse6','YC-Oracle','AUTO-fuzhi1','AUTO-Oracle10g','AUTO-Oracle11g-1','AUTO-Oracle11g-2','AUTO-Oracle11g-3','AUTO-Oracle19c','AUTO-Mysql57-UTF','AUTO-Mysql55','AUTO-Mysql56','AUTO-DB2-V11-1','AUTO-DB2-V10-5','AUTO-DB2-V11-5','AUTO-PG-12-1','AUTO-PG-9-4']
#     new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
#     new_list = list_connections1 + list_connections2
#     try:
#         for i in new_list:
#             new_conn.search_connection(i)
#             num = new_conn.get_num()
#             if num == 1:
#                 new_conn.del_connection(i)
#     except BaseException as e:
#         print('删除连接报错：{}'.format(e))


# 39.验证修改连接-连接名称和数据源类型是否置灰不可修改
@given("已进入该连接的修改页面")
def step_impl(page, pages):
    page.locator(locations_list["修改按钮"]).click()
    time.sleep(5)


@when("鼠标移入连接名称输入框、数据源类型输入框")
def step_impl(page):
    page.locator(locations_new["连接名称"]).hover()



@then("置灰显示,不可点击")
def step_impl(page):
    expect(page.locator(locations_new["连接名称"])).not_to_be_focused()
    expect(page.locator(locations_new["数据源类型"])).not_to_be_focused()


# Scenario: 40.验证修改连接-IP地址是否不可为空
@when("修改IP地址输入框内容,输入为空")
def step_impl(page):
    page.locator(locations_new["ip地址"]).fill('')


# 41、42、43
@when(parsers.parse("IP地址输入{ip}"))
def step_impl(page, ip):
    page.locator(locations_new["ip地址"]).fill(ip)


@when("修改数据库名称输入框内容,输入为空")
def step_impl(page):
    page.locator(locations_new["数据库名称"]).fill('')


@when("修改用户名输入框内容,输入为空")
def step_impl(page):
    page.locator(locations_new["用户名"]).fill('')


# Scenario: 44.验证修改连接-修改连接后,是否可以不进行隐私发现
@given(parsers.parse("该连接隐私识别状态为[{status}]"))
def step_impl(page, status):
    page.locator(locations_list["隐私识别状态"]).highlight()
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    # assert secret_status == status
    if secret_status in ["新建", "运行"]:
        for i in range(600):
            secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
            if secret_status == '新建':
                time.sleep(1)
            elif secret_status == '运行':
                time.sleep(1)
            else:
                break
    loc = "//div[contains(@class,'el-table__body-wrapper')]"
    page.locator(loc).click()
    page.mouse.wheel(10000,0)
    time.sleep(0.5)
    make_screenshot(page, case_order=12)
    assert secret_status == status


@then(parsers.parse("连接{connect_name}隐私识别状态为完成"))
def step_impl(page, pages, connect_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(connect_name)
    page.locator(locations_list["隐私识别状态"]).highlight()
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    # assert secret_status == status
    if secret_status == "运行":
        for i in range(600):
            secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
            if secret_status == '运行':
                time.sleep(1)
            elif secret_status == '完成':
                break


@when(parsers.cfparse("修改该连接发现范围,增加一个schema[{db_name}]"))
def step_impl(page, pages, db_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.part_data_db1(db_name)


@given('点击保存,"是否重新进行隐私发现"弹框中选择不需要')
def step_impl(page):
    page.locator(locations_new['保存']).click()
    page.locator("//button//span[text()='不需要']").click()

@when(parsers.cfparse('点击保存,"是否重新进行隐私发现"弹框中选择[{type}]'))
def step_impl(page, type):
    time.sleep(1)
    page.locator(locations_new['保存']).click()
    make_screenshot(page, case_order=47)
    time.sleep(1)
    page.locator("//button//span[text()='{}']".format(type)).click()


@then("回到数据连接列表页面")
def step_impl(page, pages):
    page.goto(pages['connection_page'])
    time.sleep(1)


@when("回到数据连接列表页面")
def step_impl(page, pages):
    page.goto(pages['connection_page'])
    time.sleep(2)


@then(parsers.parse("该连接连接状态为[{connect_status1}],隐私识别状态为[{secret_status1}]或[{secret_status2}]"))
def step_impl(page, pages, connect_status1, secret_status1, secret_status2, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    page.locator(locations_list["隐私识别状态"]).highlight()
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == connect_status1

    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    assert secret_status in [secret_status1, secret_status2]
    if secret_status in ['运行', '新建']:
        for i in range(600):
            secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
            if secret_status == '运行':
                time.sleep(1)
            elif secret_status == '新建':
                time.sleep(1)
            else:
                break
    assert secret_status == '完成'


@then(parsers.parse("该连接连接状态为[{connect_status1}],该连接隐私识别状态为[{secret_status1}]"))
def step_impl(page, pages, connect_status1, secret_status1, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    page.locator(locations_list["隐私识别状态"]).highlight()
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == connect_status1
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    assert secret_status == secret_status1


@then(parsers.parse("该连接连接状态为[{connect_status1}],该连接的隐私识别状态为[{secret_status1}]或[{secret_status2}]"))
def step_impl(page, pages, connect_status1, secret_status1, secret_status2, conn_name):
    time.sleep(2)
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    page.locator(locations_list["隐私识别状态"]).highlight()
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == connect_status1

    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    assert secret_status in [secret_status1, secret_status2]


# Scenario Outline: 45.验证修改连接-修改连接后,是否可以重新全量发现
@when(parsers.parse("修改发现范围,新增{find_schema1}"))
def step_impl(page, pages, find_schema1):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.part_data_db1(find_schema1)


# Scenario Outline: 46.验证修改连接-修改连接后,是否可以重新增量发现
@when(parsers.parse("修改发现范围,删除{find_schema1}"))
def step_impl(page, pages, find_schema1):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.part_data_except_db(dbname=find_schema1)


@when("修改发现范围,勾选发现全部数据")
def step_impl(page):
    page.locator(locations_new["发现全部数据源"]).click()

# Scenario Outline: 48.验证修改连接-是否可以修改保存为异常连接


@when(parsers.parse("仅修改该连接IP地址为[{ip}]"))
def step_impl(page, ip):
    page.locator(locations_new["ip地址"]).fill(ip)


@then(parsers.cfparse("该数据连接,连接状态变为[{status}]"))
def step_impl(page, pages, conn_name, status):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    connect_status = page.locator(locations_list["连接状态"]).text_content().strip(' ')
    assert connect_status == status


# 50.验证删除连接-删除是否可点击
@when('点击"更多-删除"')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    page.locator(locations_list["删除按钮"]).click()


@then('弹出确认框,提示:"删除后不可找回，是否确定删除此连接?"')
def step_impl(page):
    expect(page.locator("//span[text()='删除后不可找回，是否确定删除此连接?']")).to_be_visible()


# Scenario Outline: 51.验证删除连接-是否可以删除连接成功
@given(parsers.parse("等待该连接隐私识别结束"))
def step_impl(page):
    page.locator(locations_list["隐私识别状态"]).highlight()
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]

    if secret_status in ["新建", "运行"]:
        for i in range(600):
            secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
            if secret_status == '新建':
                time.sleep(1)
            elif secret_status == '运行':
                time.sleep(1)
            else:
                break
    loc = "//div[contains(@class,'el-table__body-wrapper')]"
    page.locator(loc).click()
    page.mouse.wheel(10000,0)
    time.sleep(0.5)
    make_screenshot(page, case_order=51)


@when('点击"删除-确定"')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    page.locator(locations_list["删除按钮"]).click()
    page.locator('button:has-text("确定")').nth(1).click()


@then('系统提示:"删除成功"')
def step_impl(page):
    page.wait_for_selector("div[role=\"alert\"]:has-text(\"删除成功\")")
    expect(page.locator("div[role=\"alert\"]:has-text(\"删除成功\")")).to_be_visible()


@then(parsers.parse("数据连接列表页,搜索{conn_name},连接不存在"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    assert num == 0


# scenario Outline: 55.验证查询连接-查询能否成功

@when(parsers.parse("连接名称输入{conn_name},数据源类型选择{db_source},IP地址输入{ip},端口输入{port},连接状态输入{conn_status},隐私识别状态选择{privacy_status},创建日期选择{create_date}"))
def step_impl(page, pages, conn_name, db_source, ip, port, conn_status, privacy_status, create_date):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_all(connection_name=conn_name, data_type=db_source, secret_status=privacy_status, ip=ip, port=port, connect_status=conn_status, date_time=create_date)


@when('点击数据连接"查询"')
def step_impl(page):
    page.locator(locations_search["查询按钮"]).click()
    time.sleep(1.5)


@then(parsers.parse("查询成功,列表筛选出满足查询条件的数据{conn_name2}"))
def step_impl(page, pages, conn_name2):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    if conn_name2 in ['NULL', 'null', '']:
        num = new_conn.get_num()
        assert num == 0
        expect(page.locator("//span[text()='暂无数据']")).to_be_visible()
    else:
        data = new_conn.get_all_line_data()
        conn_list = []
        for i in data:
            conn_name = i["其他行-连接名称"]
            conn_list.append(conn_name)
        assert conn_name2 in conn_list


# 52.验证删除连接-取消删除连接能否成功
@when('点击"取消"')
def step_impl(page):
    loc_cancel = "//div[@class='el-message-box']//button[span[text()='取消']]"
    page.locator(loc_cancel).click()


@then("回到数据连接列表页,该连接依然存在")
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    assert num == 1


# Scenario: 53.验证查询连接-查询不到数据时显示是否正确
@when(parsers.cfparse("连接名称输入[{conn_name}]"))
def step_impl(page, conn_name):
    page.locator(locations_search["连接名称"]).fill(conn_name)


@then('列表刷新,显示"暂无数据"')
def step_impl(page):
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    assert num == 0
    expect(page.locator("//span[text()='暂无数据']")).to_be_visible()


# Scenario: 54验证查询连接-查询条件重置能否成功
@when('点击"重置"')
def step_impl(page):
    page.locator(locations_search["重置按钮"]).click()
    time.sleep(1)


@then("列表刷新,返回至首页,显示所有连接信息")
def step_impl(page, pages):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    num = new_conn.get_num()
    assert num >= 1


@then("连接名称输入框内容为空")
def step_impl(page):
    content = page.locator(locations_search["连接名称"]).input_value()
    assert content == ''


# 56.验证数据连接页面-双击是否可查看连接信息


@when("鼠标双击该连接名称",target_fixture="data_dict")
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    data_dict = new_conn.get_all_line_data()[0]
    page.locator(locations_list["连接名称"]).dblclick()
    time.sleep(2)
    return data_dict


@then("弹出连接详情弹窗")
def step_impl(page, conn_name):
    loc = "//div[@class='el-dialog__header']//span[text()='{}']".format(conn_name)
    expect(page.locator(loc)).to_be_visible()


@then('包含字段:"连接名称"、"数据源类型"、"IP地址"、"端口"、"用户名"、"自定义参数"、"创建时间"、"创建人"、"连接状态"、"数据源状态"、"隐私识别状态"')
def step_impl(page):
    list1 = ['连接名称', '数据源类型', 'IP地址', '端口',"用户名", '自定义参数' ,'创建日期', '创建人', '连接状态', '数据源状态', '隐私识别状态']
    for i in list1:
        loc = locations_detail[i]
        expect(page.locator(loc)).to_be_visible()


@then('字段:"连接名称"、"数据源类型"、"IP地址"、"端口"、"创建时间"、"连接状态"、"数据源状态"、"隐私识别状态"与连接列表统计内容一致')
def step_impl(page, pages, data_dict):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    data_dict_new = new_conn.get_detail()
    list2 = ['连接名称','数据源类型','IP地址','端口','创建日期','连接状态','数据源状态','隐私识别状态']
    for key in list2:
        new_key = "其他行-" + key
        assert data_dict_new[key] == data_dict[new_key]


# Scenario: 57.验证数据连接页面-连接信息弹窗是否可以关闭

@when('点击"关闭"')
def step_impl(page):
    close_button = "//div[@class='el-dialog__body']/following-sibling::div[@class='el-dialog__footer']//button[span[text()='关闭']]"
    page.locator(close_button).click()


@then("回到数据连接列表页面1")
def step_impl(page, pages):
    assert page.url == pages['connection_page']


# Scenario: 58.验证数据连接页面-是否可以查看任务信息
@when('点击该连接的"任务信息"')
def step_impl(page):
    page.locator(locations_list['任务信息']).click()


@then("弹出任务信息弹窗")
def step_impl(page):
    loc = "//div[@class='el-dialog__header']//span[text()='隐私发现任务信息']"
    expect(page.locator(loc)).to_be_visible()


@then('弹窗左上角包含标题"隐私发现任务信息"')
def step_impl(page):
    loc = "//div[@class='el-dialog__header']//span[text()='隐私发现任务信息']"
    expect(page.locator(loc)).to_be_visible()


@then('页面展示内容包含板块:"基本信息"、"隐私发现"、"隐私判定参数"、"任务运行参数"、"任务创建信息"')
def step_impl(page):
    list_loc = ["基本信息", "隐私发现", "隐私判定参数", "任务运行参数", "任务创建信息"]
    locations = locations_detail1
    for i in list_loc:
        expect(page.locator(locations[i])).to_be_visible()


# Scenario: 60.验证数据连接页面-点击"识别结果"是否可以跳转
@when('点击该连接的"发现结果"')
def step_impl(page):
    page.locator(locations_list['识别结果']).click()
    time.sleep(2)


@then("跳转到发现结果页面1")
def step_impl(page, pages):
    assert 'findresult' in page.url


@then(parsers.cfparse("自动检索出连接名称为[{conn_name}]的发现结果"))
def step_impl(page, pages, conn_name):
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    loc = "//div[@class='el-table__virtual-wrapper']//tbody/tr[{}]/td[2]//div[@class='content-box']"
    try:
        if num > 10:
            for i in range(1,11):
                content = page.locator(loc.format(i)).text_content().strip(' ')
                assert content == conn_name
        else:
            for i in range(1, num):
                content = page.locator(loc.format(i)).text_content().strip(' ')
                assert content == conn_name
    except NotImplementedError as e:
        logger.error('No such element: {}'.format(e.args))


# Scenario: 61.验证数据连接页面-是否可以点击"测试连接"
@when('点击该连接的"测试连接"')
def step_impl(page):
    page.locator(locations_list["测试连接按钮"]).click()


@then('弹框提示:"连接成功"')
def step_impl(page):
    loc_info = "//div[@role='alert']//p"
    if page.locator(loc_info).is_visible():
        make_screenshot(page, case_order=60)
    page.wait_for_selector("div[role=\"alert\"]:has-text(\"连接成功\")")
    expect(page.locator("div[role=\"alert\"]:has-text(\"连接成功\")")).to_be_visible()


# Scenario: 62.验证数据连接页面-数据源禁用能否成功
@given(parsers.cfparse("该连接数据源状态为[{status}]"))
def step_impl(page, status):
    content = page.locator(locations_list["数据源状态"]).text_content().strip(' ')
    assert content == status


@given(parsers.cfparse("该连接数据源的状态为[{status}]"))
def step_impl(page, status):
    content = page.locator(locations_list["数据源状态"]).text_content().strip(' ')
    if content != status:
        page.locator(locations_list["更多按钮"]).click()
        page.locator(locations_list[status+'按钮']).click()
    time.sleep(2)


@when('点击"更多-禁用"')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    time.sleep(0.5)
    page.locator(locations_list["禁用按钮"]).click()


@then('弹框提示:"已禁用"')
def step_impl(page):
    page.wait_for_selector("div[role=\"alert\"]:has-text(\"已禁用\")")
    expect(page.locator("div[role=\"alert\"]:has-text(\"已禁用\")")).to_be_visible()


@then(parsers.cfparse("连接名称为[{conn_name}]的数据连接,数据源状态变更为[{status}]"))
def step_impl(page, pages, conn_name, status):
    time.sleep(1)
    content = page.locator(locations_list["数据源状态"]).text_content().strip(' ')
    assert content == status


# Scenario: 63.验证数据连接页面-数据源启用能否成功
@when('点击"更多-启用"')
def step_impl(page):
    time.sleep(1)
    page.locator(locations_list["更多按钮"]).click()
    time.sleep(1)
    page.locator(locations_list["启用按钮"]).click()


@then('弹框提示:"已启用"')
def step_impl(page):
    page.wait_for_selector("div[role=\"alert\"]:has-text(\"已启用\")")
    expect(page.locator("div[role=\"alert\"]:has-text(\"已启用\")")).to_be_visible()


# Scenario Outline: 64.验证数据连接页面-数据源重新隐私发现能否成功
@when('点击"更多-重新隐私发现"')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    page.locator(locations_list["重新隐私发现"]).click()


@then(parsers.parse('提示：需要对{conn_name}进行重新隐私发现吗'))
def step_impl(page, conn_name):
    # loc = "//div[@class="el-dialog__body"]//div[text()="需要对【HIVEan】进行重新隐私发现吗？"]"
    text_loc = "//div[@class='el-dialog__body']//div[text()='需要对【{}】进行重新隐私发现吗？']".format(conn_name)
    page.wait_for_selector(text_loc)
    expect(page.locator(text_loc)).to_be_visible()


@when('点击"全量发现"')
def step_impl(page):
    page.locator("button:has-text(\"全量发现\")").click()


@then("触发隐私发现成功")
def step_impl(page):
    page.wait_for_selector("p:has-text(\"已重新发现\")")
    expect(page.locator("p:has-text(\"已重新发现\")")).to_be_visible()


@then(parsers.parse("{conn_name}隐私识别状态变为运行"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    assert secret_status in ["运行", '完成']


@then('"重新隐私发现"按钮置灰不可点击')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    expect(page.locator(locations_list["重新隐私发现"])).not_to_be_focused()
    time.sleep(1)


# Scenario: 65.验证数据连接页面-数据源终止隐私发现能否成功
@given(data_table('页面存在发现全部数据源的数据连接B,不存在则新建', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(sql_type=data_list[0]["db_source"], data_values=data_list[0])
    time.sleep(1.5)
    new_conn.search_connection(conn_name)
    return conn_name


@given("该连接的隐私识别状态为[运行]")
def step_impl(page):
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    if secret_status != "运行":
        page.locator(locations_list["更多按钮"]).click()
        time.sleep(0.2)
        page.locator(locations_list["重新隐私发现"]).click()
        time.sleep(0.2)
        page.locator("button:has-text(\"全量发现\")").click()
        time.sleep(0.2)


@when('鼠标移入"更多"选项下')
def step_impl(page):
    page.locator(locations_list["更多按钮"]).click()
    time.sleep(0.7)


@when('点击"终止隐私发现"')
def step_impl(page):
    # page.wait_for_selector(locations_list["终止隐私发现"]).hover()
    # for i in range(20):
    #     check = page.locator(locations_list["终止隐私发现"]).focus()
    #     if check:
    #         page.locator(locations_list["终止隐私发现"]).click()
    #         break
    #     time.sleep(0.15)
    page.locator(locations_list["终止隐私发现"]).click()


@then('弹框提示:"已终止隐私发现"')
def step_impl(page):
    page.wait_for_selector("div[role=\"alert\"]:has-text(\"已终止隐私发现\")")
    expect(page.locator("div[role=\"alert\"]:has-text(\"已终止隐私发现\")")).to_be_visible()
    loc_info = "//div[@role='alert']//p"
    if page.locator(loc_info).is_visible():
        make_screenshot(page, case_order=65)


@then(parsers.cfparse("数据连接[{conn_name}]隐私识别状态变为[{status}]"))
def step_impl(page, conn_name, status):
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    assert secret_status == status


@when('鼠标悬浮移入隐私识别状态"终止"的字段上')
def step_impl(page):
    page.locator(locations_list["隐私识别状态"]).hover()


@then('展示终止原因包含字段"任务手动终止"')
def step_impl(page):
    warning_loc = "//div[@role='tooltip' and @aria-hidden='false']//div[@class='step-warning']//span[text()='任务手动终止 ']"
    time.sleep(1)
    expect(page.locator(warning_loc)).to_be_visible()


@given(data_table('存在发现部分数据源的数据连接C,不存在则新建', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(sql_type=data_list[0]["db_source"], data_values=data_list[0], dbname='autotest1')
    time.sleep(1.5)
    new_conn.wait_for_find_finished(conn_name)
    return conn_name


@then(parsers.cfparse("搜索和查询数据连接[{conn_name}]存在"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    time.sleep(1)
    num = new_conn.get_num()
    assert num == 1


@when("进入数据连接列表页")
def step_impl(page, pages):
    page.goto(pages['connection_page'])
    time.sleep(0.5)


@then(parsers.cfparse("删除数据连接[{conn_name}]成功"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    time.sleep(1)
    new_conn.del_connection(conn_name)


@given(data_table('使用下方参数，创建hive目标端数据连接', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(connect_type='数据库', target='目标端', sql_type=data_list[0]["db_source"], data_values=data_list[0], save_type=data_list[0]['save_type'])
    time.sleep(2)
    return conn_name


@given(data_table('使用下方参数，创建mysql目标端数据连接', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(connect_type='数据库', target='目标端', sql_type=data_list[0]["db_source"], data_values=data_list[0])
    make_screenshot(page, case_order=69)
    time.sleep(2)
    return conn_name


@given(data_table('使用下方参数，创建文件-源端-FTP数据连接', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(connect_type='文件', file_connect_type=data_list[0]["file_connect_type"], target=data_list[0]['target'], data_values=data_list[0])
    make_screenshot(page,case_order=67)
    time.sleep(2)


@given(data_table('使用下方参数，创建文件-目标端-oss数据连接', fixture='data_list'), target_fixture="conn_name")
def step_impl(page, pages, data_list):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = data_list[0]["conn_name"]
    new_conn.search_connection(conn_name)
    num = new_conn.get_num()
    if num == 0:
        new_conn.new_connection(connect_type='文件', file_connect_type=data_list[0]["file_connect_type"], target=data_list[0]['target'], data_values=data_list[0])
    make_screenshot(page,case_order=67)
    time.sleep(2)


@when(parsers.parse("等待数据连接{conn_name}-隐私发现完成"))
def step_impl(page, pages, conn_name):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    new_conn.search_connection(conn_name)
    page.locator(locations_list["隐私识别状态"]).highlight()
    secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
    # assert secret_status == status
    if secret_status in ["运行"]:
        for i in range(600):
            secret_status = page.locator(locations_list["隐私识别状态"]).text_content().split(' ')[-1]
            if secret_status in ["运行"]:
                time.sleep(1)
            elif secret_status == '完成':
                break


@when(parsers.cfparse("数据连接-等待[{tt}]s"))
def step_impl(page, tt):
    time.sleep(int(tt))

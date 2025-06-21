import allure

from common.data_table import data_table
from playwright.sync_api import expect
from pytest_bdd import scenarios, given, when, then, parsers
from loguru import logger
import time
import datetime
from pages.common.connection_page import ConnectionPage
from common.get_location import get_locations
# from pages.common.secret_plan_page import SecretPlan, SecretType
# from pages.common.mask_plan_page import MaskPlan
from pages.common.mask_task_page import MaskTaskPage
from common.sql_connect import MySql
from pages.dta.risk_analysis_page import RiskAnalysisPage

locations_mask_task = get_locations(page_name='脱敏任务', module_name='列表部分')
locations_search = get_locations(page_name='风险分析-全局', module_name='查询')
locations_list = get_locations(page_name='风险分析-全局', module_name='列表')
locations_risk_detail = get_locations(page_name='风险分析-全局', module_name='风险分析-详情页')
locations_conn_detail = get_locations(page_name='风险分析-全局', module_name='数据源-详情页')
locations_general = get_locations(page_name='风险分析-全局', module_name='其他')
locations_user = get_locations(page_name='风险分析-全局', module_name='访问用户')
locations_data_source = get_locations(page_name='风险分析-全局', module_name='数据源')


scenarios('./dta/自动化用例-风险分析-单模块.feature')
logger.add('../logs/mylogs/{}.txt'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))

today = str(datetime.date.today()).replace('-', '')


def make_screenshot(page, case_order):
    time_stamp = str(time.time() * 1000).split('.')[0]
    allure.attach(page.screenshot(path='./test_data/screen_shots/用例{}_{}.png'.format(str(case_order), time_stamp)),
                  '页面截图_用例{}_{}'.format(str(case_order), time_stamp), allure.attachment_type.PNG)


# 背景
# @given("用户已登录数据访问网关平台1")
# def step_impl(page, pages):
#     new_login = LoginPage(base_url=pages['connection_page'], page=page)
#     new_login.login('shenpengfei1','!Qaz2wsx')

@given("用户已登录数据访问网关平台1")
def step_impl(page):
    pass


@given(data_table("已经存在mysql数据连接B,不存在则新建",fixture="conn_data"))
def step_impl(page, pages, conn_data):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    for i in range(len(conn_data)):
        conn_list = conn_data[i]
        conn_name = conn_list['conn_name']
        new_conn.search_connection(conn_name)
        num = new_conn.get_num()
        if num == 0:
            new_conn.new_connection(sql_type=conn_list["db_source"], data_values=conn_list, dbname=conn_list["find_schema"])
            time.sleep(2)


@given(data_table("存在下方脱敏任务B，不存在则新建", fixture="new_data"), target_fixture="task_name")
def step_impl(page, pages, new_data):
    new_task = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    for i in range(len(new_data)):
        access_group = new_data[i]["access_group"]
        task_name = new_data[i]["task_name"]
        data_source = new_data[i]["conn_name"]
        data_list = [task_name, data_source]

        new_task.search_visit_group(group_name=access_group)
        if new_task.get_num() == 0:
            new_task.new_visit_group(group_name=access_group)

        new_task.search(task_name=task_name)
        if new_task.get_num() == 0:
            new_task.new_task_fill(data_list=data_list, visit_group=access_group)
        time.sleep(1.2)
        new_task.search(task_name=task_name)


@given(parsers.cfparse("脱敏任务[{task_name}]的代理端口为B"), target_fixture="port")
def step_impl(page, pages, task_name):
    time.sleep(1)
    new_mask = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    new_mask.search(task_name)
    time.sleep(1)
    port = page.locator(locations_mask_task["列表-首行-数据-端口"]).text_content().strip(' ')
    return port


@given(parsers.cfparse("脱敏任务[{task_name}]已正常启动"))
def step_impl(page, pages, task_name):
    time.sleep(1.2)
    check = "is-disabled"
    add_loc = "/parent::a"
    new_task = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    new_task.search(task_name)
    time.sleep(1.2)
    if page.locator(locations_mask_task["列表-首行-按钮-提交"]).is_visible():
        if check not in page.locator(locations_mask_task["列表-首行-按钮-提交"] + add_loc).get_attribute('class'):
            page.locator(locations_mask_task["列表-首行-按钮-提交"]).click()
            time.sleep(1.2)
    new_task.search(task_name)
    if page.locator(locations_mask_task["列表-首行-按钮-审批"]).is_visible():
        if check not in page.locator(locations_mask_task["列表-首行-按钮-审批"] + add_loc).get_attribute('class'):
            page.locator(locations_mask_task["列表-首行-按钮-审批"]).click()
            time.sleep(2)
            page.locator(locations_mask_task["审批通过按钮"]).click()
            time.sleep(3)
    new_task.search(task_name)
    if page.locator(locations_mask_task["列表-首行-按钮-启动"]).is_visible():
        if check not in page.locator(locations_mask_task["列表-首行-按钮-启动"] + add_loc).get_attribute('class'):
            page.locator(locations_mask_task["列表-首行-按钮-启动"]).click()
            time.sleep(2)


@given(data_table("存在脱敏任务代理端连接B，并执行以下sql访问", fixture="sql_list"))
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456', dbname='autotest1')
    for sql in sql_list:
        real_sql = sql["sql_command"]
        try:
            new_sql_conn.execute_sql(real_sql)
            time.sleep(0.2)
        except ConnectionError as e:
            logger.info("连接执行失败：{}".format(e.args))
        finally:
            logger.info("pass")
    new_sql_conn.close()
    time.sleep(2)


@given(data_table("存在脱敏任务代理端连接D，并执行以下sql访问", fixture="sql_list"))
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456', dbname='autotest1')
    for sql in sql_list:
        real_sql = sql["sql_command"]
        try:
            new_sql_conn.execute_sql(real_sql)
            time.sleep(3)
        except ConnectionError as e:
            logger.info("连接执行失败：{}".format(e.args))
        finally:
            logger.info("pass")
    new_sql_conn.close()
    time.sleep(2)


@given("页面跳转至风险分析页面")
def step_impl(page, pages):
    # page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    page.goto(pages["risk_analysis_page"])
    time.sleep(2)


# 用例1-验证全局信息页面布局是否正确
@given("已进入风险分析-全局信息页面")
def step_impl(page, pages):
    page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    time.sleep(1.2)
    page.locator("//div[@role='tablist']//div[text()='全局信息']").click()
    time.sleep(1.2)


@when("查看所有页签时")
def step_impl():
    pass


@then('从左到右依次展示："全局信息"、"访问用户"、"数据源"、"＋新增"')
def step_impl(page):
    all_text = page.locator(locations_general["顶部页签"]).all_text_contents()
    list_name = ["全局信息", "访问用户", "数据源"]
    for name in list_name:
        assert name in all_text
    expect(page.locator(locations_general["顶部新增图标"])).to_be_visible()


@when("查看搜索条件时")
def step_impl():
    pass


@then('从左到右依次展示："会话状态"、"任务名称"、"风险等级"、"执行结果"')
def step_impl(page):
    base_loc = "//div[@class='search-form-item']/div//label"
    all_text = page.locator(base_loc).all_text_contents()
    name_list = ["会话状态", "任务名称", "风险等级", "执行结果"]
    for i in range(4):
        assert name_list[i] in all_text[i]


@then('搜索条件上部依次展示："更多搜索"链接、"重置"按钮、"查询"按钮')
def step_impl(page):
    loc_list = ["更多搜索", "查询按钮", "重置按钮"]
    for loc in loc_list:
        new_loc = locations_search[loc]
        expect(page.locator(new_loc)).to_be_visible()


@when("查看列表信息时")
def step_impl():
    pass


@then('从左到右依次展示："任务名称"、"数据源"、"会话编号"、"会话状态"、"SQL编号"、"SQL语句"、"访问用户IP"、"访问时间"、"执行结果"、"风险等级"、"安全操作"、"脱敏操作"')
def step_impl(page):
    name_list = ["任务名称", "数据源", "会话编号", "会话状态", "SQL编号", "SQL语句", "访问用户IP", "访问时间", "执行结果", "风险等级", "安全操作", "脱敏操作"]
    all_text = page.locator(locations_list["表头行"]).all_text_contents()
    for name in name_list:
        assert name in all_text


# 用例2-验证全局信息"更多搜索"是否可点击
@when('点击"更多搜索"')
def step_impl(page):
    page.locator(locations_search["更多搜索"]).click()
    time.sleep(1.2)
    time.sleep(0.5)


@then("弹出多选页面")
def step_impl(page):
    expect(page.locator(locations_search["更多搜索下拉框"])).to_be_visible()


@when('点击更多搜索-"全选"')
def step_impl(page):
    page.locator(locations_search["更多搜索-全选"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


@then("所有选项均被勾选成功")
def step_impl(page):
    locators = page.locator(locations_search["更多搜索-所有勾选框"])
    count = locators.count()
    for i in range(count):
        check = locators.nth(i).is_checked()
        assert check


# 用例3-验证全局信息"更多搜索"弹出框是否可勾选单个或多个
@when(parsers.cfparse('搜索选项勾选[{content}]时'))
def step_impl(page, content):
    content_list = content.split(',')
    for tt in content_list:
        page.locator(locations_search["更多搜索-按名称勾选"].format(tt)).click()
    time.sleep(1.2)


@then(parsers.cfparse('查询项增加字段[{add_text}]'))
def step_impl(page, add_text):
    add_list = add_text.split(',')
    base_loc = locations_search["所有搜索框-上方文本"]
    for add in add_list:
        new_loc = base_loc.format(add)
        expect(page.locator(new_loc)).to_be_visible()


# 用例4-验证全局信息查询条件是否支持单选和多选
@when("风险分析搜索取消全选")
def step_impl(page):
    page.locator(locations_search["更多搜索"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["更多搜索-全选"]).click()
    time.sleep(1.2)
    time.sleep(0.2)
    page.locator(locations_search["更多搜索-全选"]).click()
    time.sleep(1.2)


@when(parsers.cfparse("查询条件增加[{choice}]-内容选择[{content}]"))
def step_impl(page, choice, content):
    page.locator(locations_search["更多搜索-按名称勾选"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["搜索框-输入-按文本"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["下拉框-按文本"].format(content)).click()
    time.sleep(1.2)
    time.sleep(0.5)


@when(parsers.cfparse("查询条件再次增加[{choice}]-内容选择[{content}]"))
def step_impl(page, choice, content):
    page.locator(locations_search["更多搜索"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["更多搜索-按名称勾选"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["搜索框-输入-按文本"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["下拉框-按文本"].format(content)).click()
    time.sleep(1.2)
    time.sleep(0.5)


@when("点击风险分析查询按钮")
def step_impl(page):
    page.locator(locations_search["查询按钮"]).click()
    time.sleep(2)
    time.sleep(1.2)


@then("列表展示会话状态为断开的记录信息")
def step_impl(page):
    base_loc = "//div[@class='main-table']//div[contains(@class,'el-table__body-wrapper')]//tbody/tr[{}]//td"
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    if num > 10:
        num = 10
    for i in range(1, num+1):
        content = page.locator(base_loc.format(str(i))).all_text_contents()
        assert content[3] == "断开"


@then("列表展示风险低、执行成功的记录信息")
def step_impl(page):
    base_loc = "//div[@class='main-table']//div[contains(@class,'el-table__body-wrapper')]//tbody/tr[{}]//td"
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    if num > 10:
        num = 10
    for i in range(1, num+1):
        content = page.locator(base_loc.format(str(i))).all_text_contents()
        assert content[8] == "成功"
        assert content[9] == "无"


# 用例5-验证全局信息查询条件重置功能是否正常
@when(parsers.cfparse("查询条件增加[{choice}]-内容输入[{content}]"))
def step_impl(page, choice, content):
    page.locator(locations_search["更多搜索"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["更多搜索-按名称勾选"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["搜索框-输入-按文本"].format(choice)).fill(content)


@when('点击风险分析查询"重置"按钮')
def step_impl(page):
    page.locator(locations_search["重置按钮"]).click()
    time.sleep(1.2)


@then("数据源内容清除为空")
def step_impl(page):
    page.locator(locations_search["搜索框-输入-按文本"].format("数据源")).highlight()
    content = page.locator(locations_search["搜索框-输入-按文本"].format("数据源")).input_value()
    assert content == ""


# 用例6-验证全局信息列表右侧的"+"是否可点击
@when('点击列表右侧的"+"')
def step_impl(page):
    page.locator(locations_search["右侧-增加"]).click()
    time.sleep(1.2)


@then("正常弹出多选框")
def step_impl(page):
    loc = locations_search["右侧-增加-列表框"]
    expect(page.locator(loc)).to_be_visible()


# 用例7-验证全局信息列表右侧的"+"是否可单选或多选

@when(parsers.cfparse("列新增勾选选项[{choice}]"))
def step_impl(page, choice):
    choice_list = choice.split(',')
    for cc in choice_list:
        loc = locations_search["右侧-增加-勾选-按文本"].format(cc)
        page.locator(loc).click()
    time.sleep(1.2)


@when('点击新增"确定"')
def step_impl(page):
    page.locator(locations_search["右侧-增加-确定按钮"]).click()
    time.sleep(1.2)


@then(parsers.cfparse("列表最右侧新增列[{add_text}]"))
def step_impl(page, add_text):
    add_list = add_text.split(',')
    base_loc = locations_list["表头行"]
    all_text = page.locator(base_loc).all_text_contents()
    for column in add_list:
        assert column in all_text


@when('点击勾选"全选"')
def step_impl(page):
    page.locator(locations_search["右侧-增加-全选"]).click()
    time.sleep(1.2)


@then("所有选项均被勾选")
def step_impl(page):
    locators = page.locator(locations_search["右侧-增加-勾选-列表"])
    num = locators.count()
    for i in range(num):
        check = locators.nth(i).is_checked()
        assert check


# 用例8-验证全局信息列表右侧的"+"是否可取消勾选
@when(parsers.cfparse("取消勾选[{choice}]"))
def step_impl(page, choice):
    choice_list = choice.split(',')
    for cc in choice_list:
        loc = locations_search["右侧-增加-勾选-按文本"].format(cc)
        page.locator(loc).click()
    time.sleep(1.2)


@then(parsers.cfparse("列表最右侧去掉两列[{del_text}]"))
def step_impl(page, del_text):
    del_list = del_text.split(',')
    base_loc = locations_list["表头行"]
    all_text = page.locator(base_loc).all_text_contents()
    for column in del_list:
        assert column not in all_text


# 用例9-验证双击列表中的任意一行数据，是否可以弹出SQL语句详情
@given("风险分析的全局页面-列表中存在数据")
def step_impl(page):
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    assert num >= 1


@when("双击列表第一行数据")
def step_impl(page):
    page.locator(locations_list["首行-sql语句"]).dblclick()
    time.sleep(2)


@then("可以弹出SQL语句详情页")
def step_impl(page):
    expect(page.locator(locations_risk_detail["弹框主体"])).to_be_visible()


# 用例10-验证全局信息列表中的数据源，是否可点击
@when('点击列表首行"数据源"对应链接时')
def step_impl(page):
    page.locator(locations_list["首行-数据源"]).click()
    time.sleep(1.2)


@then("可弹出数据源详情页")
def step_impl(page):
    expect(page.locator(locations_conn_detail["标题可见"])).to_be_visible()


# 用例11-验证全局信息列表中的数据源，是否可点击
@when('点击首行"SQL编号"下的链接时')
def step_impl(page):
    page.locator(locations_list["首行-sql编号"]).click()
    time.sleep(1.2)


# 用例12-验证全局信息默认审计状态下，列表是否能查看到默认审计类型的语句
@when(parsers.cfparse("增加搜索条件[{choice}]"))
def step_impl(page, choice):
    page.locator(locations_search["更多搜索"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_search["更多搜索-按名称勾选"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(0.5)


@when("清空已选SQL功能类型")
def step_impl(page):
    page.locator(locations_search["sql功能类型-下拉图标"]).hover()
    time.sleep(1.5)
    page.locator(locations_search["sql功能类型-下拉清空"]).click()
    time.sleep(1.5)


@when(parsers.cfparse("增加列表列[{choice}]"))
def step_impl(page, choice):
    page.locator(locations_search["右侧-增加"]).click()
    time.sleep(1.2)
    time.sleep(1.2)
    choice_list = choice.split(',')
    for cc in choice_list:
        loc = locations_search["右侧-增加-勾选-按文本"].format(cc)
        page.locator(loc).click()
    time.sleep(1.2)
    page.locator(locations_search["右侧-增加-确定按钮"]).click()
    time.sleep(2)


@when(parsers.cfparse("选择搜索条件[{add_text}]为[{content}]"))
def step_impl(page, add_text, content):
    page.locator(locations_search["sql功能类型-输入框"]).click()
    time.sleep(1.2)
    time.sleep(0.2)
    page.locator(locations_search["下拉框-按文本"].format(content)).click()
    time.sleep(1.2)


@then(parsers.cfparse("风险分析全局信息中将展示[{column}]为[{content}]的数据"))
def step_impl(page, column, content):
    thead_list = page.locator(locations_list["表头行"]).all_text_contents()
    index_num = thead_list.index(column)
    lines = page.locator(locations_list["列表-行数"]).count()
    list_temp = []
    for i in range(1, lines+1):
        base_loc = locations_list["列表-所有行-某列"].format(str(i),str(index_num+1))
        tt1 = page.locator(base_loc).text_content()
        tt2 = tt1.split(' ')[-2]
        list_temp.append(tt2)
    assert len(set(list_temp)) == 1
    assert list_temp[0] == content


# 用例13-验证全局信息-页面分页器能否正常使用
@when("查看全局信息页面的列表时")
def step_impl():
    pass


@then("分页器默认展示第一页的列表数据")
def step_impl(page):
    content = page.locator(locations_list["前往页码内容"]).input_value().strip(' ')
    assert content == '1'


@then("向左的箭头置灰无法点击")
def step_impl(page):
    check = page.locator(locations_list["上一页"]).is_disabled()
    assert check


@when("全局信息页面展示多页的列表数据")
def step_impl(page):
    num = int(page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
    assert num > 10


@when("全局信息页面列表翻到最后一页")
def step_impl(page):
    # locators = page.locator(locations_list["页码列表"])
    # count = locators.count()
    # page.locator(locations_list["点击页码"].format(str(count))).click()
    time.sleep(1.2)
    # time.sleep(0.5)
    # loc = ".el-pager > li"
    page.locator(".el-pager > li >> nth=-1").click()
    time.sleep(1.2)


@then("向右的箭头置灰无法点击")
def step_impl(page):
    check = page.locator(locations_list["下一页"]).is_disabled()
    assert check


@when(parsers.cfparse("在分页器中输入页码[{page_num}]"),target_fixture="page_num")
def step_impl(page, page_num):
    page.locator(locations_list["前往页码内容"]).fill(page_num)
    return page_num


@when("点击enter键")
def step_impl(page):
    page.keyboard.press('Enter')
    time.sleep(0.5)


@then("页面列表自动跳转到对应的页数")
def step_impl(page, page_num):
    content = page.locator(locations_list["前往页码内容"]).input_value().strip(' ')
    assert content == page_num


@when("在分页器中选择展示20条/页")
def step_impl(page):
    page.locator(locations_list["每页展示条数"]).click()
    time.sleep(1.2)
    page.locator(locations_list["每页展示条数下拉选择"].format('20')).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then("列表每页展示小于等于20条数据")
def step_impl(page):
    num = page.locator(locations_list["列表-行数"]).count()
    assert num <= 20


# 用例14-验证"访问用户"页存在SQL语句，SQL详情页显示名称和位置是否正确
@given("已进入风险分析-访问用户页面")
def step_impl(page, pages):
    page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    page.locator("//div[@role='tablist']//div[text()='访问用户']").click()
    time.sleep(3)


@when("点击访问用户-最新用户ip-首条数据源")
def step_impl(page):
    count = page.locator(locations_user["左侧-访问用户ip条数"]).count()
    page.locator(locations_user["左侧-某条访问用户ip点击"].format(count)).click()
    time.sleep(2)
    page.locator(locations_user["左侧-某条ip展开-首个数据源"].format(count)).click()
    time.sleep(3)


@when("点击访问用户-最新的用户ip")
def step_impl(page):
    count = page.locator(locations_user["左侧-访问用户ip条数"]).count()
    page.locator(locations_user["左侧-某条访问用户ip点击"].format(count)).click()
    time.sleep(3)


@then("访问用户IP页存在SQL语句")
def step_impl(page):
    content = page.locator(locations_user["sql操作条数"]).text_content()
    num = int(content.split('：')[-1].strip(' ')[:-1])
    assert num >= 1


@when("点击会话编号文本框下部的首行SQL语句时")
def step_impl(page):
    page.locator(locations_user["某行-sql语句点击"].format('1')).click()
    time.sleep(1.2)
    time.sleep(2)


@then('弹出SQL详情页，从上到下依次显示："风险等级"、"执行者信息"、"访问对象信息"、"执行内容信息"、"操作执行结果"、"安全防护"、"平台处理结果"')
def step_impl(page):
    target_list = ["风险等级", "执行者信息", "访问对象信息", "执行内容信息", "操作执行结果", "安全防护", "平台处理结果"]
    page.locator(locations_user["sql详情-所有title"]).highlight()
    all_text = page.locator(locations_user["sql详情-所有title"]).all_text_contents()
    assert all_text == target_list


# 用例15-验证"访问用户"页存在SQL语句，SQL详情页"风险等级"显示名称和位置是否正确

@then('SQL详情页-风险等级部分，包含风险信息，且风险等级有颜色标识，枚举值从左到右依次显示："高风险"、"中风险"、"低风险"、"无风险"')
def step_impl(page):
    list1 = ["高风险", "中风险", "低风险", "无风险"]
    all_text = page.locator(locations_user["风险等级列表"]).all_text_contents()
    new_list = [i.strip(' ') for i in all_text]
    assert list1 == new_list
    expect(page.locator(locations_user["风险提示字段"])).to_be_visible()


# 用例16-验证"访问用户"页存在SQL语句，SQL详情页"风险信息"显示内容是否正确
@then('SQL详情页显示的风险信息为操作风险的具体描述信息或"-"')
def step_impl(page):
    content = page.locator(locations_user["风险提示内容"]).text_content().strip(' ')
    assert content == '-' or content != ''


# 用例17-验证"访问用户"页存在SQL语句，SQL详情页"执行者信息"显示名称和位置是否正确
@then('执行者信息部分，依次从左到右显示："访问分组"、"访问用户IP"、"数据库用户"、"个人用户"、"客户端工具"、"访问时间"')
def step_impl(page):
    add_loc = "//div//label"
    base_loc = locations_user["sql详情-不同模块div-按文本"].format("执行者信息")
    new_loc = base_loc + add_loc
    all_text = page.locator(new_loc).all_text_contents()
    tar_list = ["访问分组", "访问用户IP", "数据库用户", "个人用户", "客户端工具", "访问时间"]
    real_list = [i.split(":")[0] for i in all_text]
    assert real_list == tar_list


# 用例18-验证"访问用户"页存在SQL语句，SQL详情页"执行者信息"显示内容是否正确
@then(parsers.cfparse("SQL详情页显示的执行者信息[{key}]内容非空"))
def step_impl(page, key):
    add_loc = "/following-sibling::div"
    base_loc = locations_user["执行者信息-字段"]
    list1 = page.locator(base_loc).all_text_contents()
    new_list = [i.split(':')[0] for i in list1]
    list2 = page.locator(base_loc+add_loc).all_text_contents()
    dict_temp = dict(zip(new_list,list2))
    assert dict_temp[key] != ""


# 用例19-验证"访问用户"页存在SQL语句，SQL详情页"访问对象信息"显示名称和位置是否正确
@then('SQL详情页访问对象信息部分，依次显示："数据库地址"、"数据库端口"、"影响对象"')
def step_impl(page):
    loc = locations_user["sql详情-不同模块div-按文本"].format("访问对象信息") + locations_user["字段补充"]
    all_text = page.locator(loc).all_text_contents()
    new_list = [i.split(':')[0] for i in all_text]
    list1 = ["数据库地址", "数据库端口", "影响对象"]
    assert list1 == new_list


# 用例20-验证"访问用户"页存在SQL语句，SQL详情页"访问对象信息"显示内容是否正确
@then(parsers.cfparse("SQL详情页-访问对象信息[{key}]内容非空"))
def step_impl(page, key):
    loc1 = locations_user["sql详情-不同模块div-按文本"].format("访问对象信息") + locations_user["字段补充"]
    all_text1 = page.locator(loc1).all_text_contents()
    new_list1 = [i.split(':')[0] for i in all_text1]
    loc2 = loc1 + locations_user["内容补充"]
    all_text2 = page.locator(loc2).all_text_contents()
    dict_temp = dict(zip(new_list1, all_text2))
    assert dict_temp[key] != ""


# 用例21-验证"访问用户"页存在SQL语句，SQL详情页"执行内容信息"显示名称和位置是否正确
@then(parsers.cfparse('SQL详情页-[{part}]部分，字段依次显示：[{columns}]'))
def step_impl(page, part, columns):
    loc = locations_user["sql详情-不同模块div-按文本"].format(part) + locations_user["字段补充"]
    all_text = page.locator(loc).all_text_contents()
    new_list = [i.split(':')[0] for i in all_text]
    column_list = columns.split(',')
    assert column_list == new_list


# 用例22-验证"访问用户"页存在SQL语句，SQL详情页"执行内容信息"显示内容是否正确
@then(parsers.cfparse("SQL详情页-[{part}]部分， 字段内容非空"))
def step_impl(page, part):
    loc = locations_user["sql详情-不同模块div-按文本"].format(part) + locations_user["字段补充"] + locations_user["内容补充"]
    all_text = page.locator(loc).all_text_contents()
    for tt in all_text:
        assert tt != ""


# 用例25-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"显示名称和位置是否正确
@then('SQL详情页-[安全防护]显示："SQL操作"、"安全操作"、"脱敏操作"')
def step_impl(page):
    loc1 = "//div[text()='安全操作 ']"
    loc2 = "//div[text()='脱敏操作 ']"
    expect(page.locator(loc1)).to_be_visible()
    expect(page.locator(loc2)).to_be_visible()


# 用例26-验证"访问用户"页存在SQL语句，SQL详情页"平台处理结果"显示内容是否正确
@then(parsers.cfparse('SQL详情页的[{part}]内容显示"处理结果"为"成功"或"失败"'))
def step_impl(page, part):
    loc = locations_user["sql详情-不同模块div-按文本"].format(part) + locations_user["字段补充"] + locations_user["内容补充"]
    content = page.locator(loc).all_text_contents()
    assert content[0].strip(' ') in ["成功", "失败"]


# 用例27-【风险分析】验证"访问用户"页签的用户数统计是否正确
@when('点击"访问用户"页签时')
def step_impl(page):
    page.locator("//div[@role='tablist']//div[text()='访问用户']").click()
    time.sleep(1.2)
    time.sleep(1.2)


@then(parsers.cfparse('标签页名称变为[{tag_name}]'))
def step_impl(page, tag_name):
    loc = "//div[@role='tablist']/div[@id='tab--2']"
    content = page.locator(loc).text_content()
    assert content == tag_name


# 用例28-【风险分析】验证访问用户页的查询条件和按钮的名称和位置是否正确
@then('查询条件依次包含文本框:"访问IP:"、"时间范围"')
def step_impl(page):
    expect(page.locator(locations_user["查询-ip"])).to_be_visible()
    expect(page.locator(locations_user["查询-时间范围-开始"])).to_be_visible()


@then('按钮名称显示："重置"、"查询"')
def step_impl(page):
    expect(page.locator(locations_user["查询按钮"])).to_be_visible()
    expect(page.locator(locations_user["重置按钮"])).to_be_visible()


@then(parsers.cfparse("访问IP-默认提示文本：[{info}]"))
def step_impl(page, info):
    content = page.locator(locations_user["查询-ip输入框"]).get_attribute("placeholder")
    assert content == info


# 用例29-【风险分析】验证访问用户页的单个查询功能是否正常

@when(parsers.cfparse("访问IP输入为[{ip}]"))
def step_impl(page, ip):
    page.locator(locations_user["查询-ip"]).fill(ip)


@when('点击"访问用户"页面的"查询"按钮')
def step_impl(page):
    page.locator(locations_user["查询按钮"]).click()
    time.sleep(2)


@then(parsers.cfparse("可以查询出访问IP为[{result}]的用户信息"))
def step_impl(page, result):
    loc = "//div[text()='访问用户IP：']/following-sibling::div"
    content = page.locator(loc).text_content().strip(' ')
    assert content == result


# 用例30-【风险分析】验证访问用户IP页的组合查询功能是否正常
@when(parsers.parse("选择多个查询条件{access_ip}、{start_time}、{end_time}"))
def step_impl(page, access_ip, start_time, end_time):
    page.locator(locations_user["查询-ip"]).fill(access_ip)
    page.locator(locations_user["查询-时间范围-开始"]).fill(start_time)
    page.locator(locations_user["查询-时间范围-结束"]).fill(end_time)


@when('点击用户ip页面-风险分析"查询"按钮')
def step_impl(page):
    page.locator(locations_user["查询按钮"]).click()
    time.sleep(1.2)


@then(parsers.parse("可以查询出该条件下的{result}数据"))
def step_impl(page, result):
    loc = "//div[text()='访问用户IP：']/following-sibling::div"
    content = page.locator(loc).text_content().strip(' ')
    assert content == result


# 用例31-【风险分析】验证访问用户IP页的重置按钮功能是否正常
@when(parsers.cfparse('"访问IP"输入为[{ip_text}]'))
def step_impl(page, ip_text):
    page.locator(locations_user["查询-ip输入框"]).fill(ip_text)


@when('点击"访问用户"页面的"重置"按钮')
def step_impl(page):
    page.locator(locations_user["重置按钮"]).click()
    time.sleep(1.2)


@then("查询条件ip内容清空")
def step_impl(page):
    content = page.locator(locations_user["查询-ip输入框"]).input_value()
    assert content == ''


# 用例32-【风险分析】验证访问用户IP页的"访问用户IP"不支持模糊查询
@given("当前页面首行ip地址为A", target_fixture="ip_text")
def step_impl(page):
    ip_text = page.locator(locations_user["左侧-ip内容"]).text_content().strip(' ')
    return ip_text


@when('输入"访问IP"A的前半部分')
def step_impl(page, ip_text):
    content = ip_text.split('.')[0] + '.' + ip_text.split('.')[1]
    page.locator(locations_user["查询-ip输入框"]).fill(content)


@then("系统不支持模糊查询，无法查询出结果")
def step_impl(page):
    assert page.locator(locations_user["左侧-ip内容"]).count() == 0


# 用例33-【风险分析】验证访问用户IP页左侧的"访问IP"可折叠
@when("展开首个卡片")
def step_impl(page):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(1.2)


@then("卡片展开成功")
def step_impl(page):
    expect(page.locator(locations_user["左侧收起图标"])).to_be_visible()


@when("收起首个卡片")
def step_impl(page):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(1.2)


@then("卡片收起成功")
def step_impl(page):
    expect(page.locator(locations_user["左侧展开图标"])).to_be_visible()


# 用例34-【风险分析】验证访问用户IP页左侧内容是否最新数据源
@then(parsers.cfparse("页面左侧最上方显示最新访问的一个数据源[{data_source}]"))
def step_impl(page, data_source):
    source = page.locator(locations_user["左侧-首个数据源"]).text_content().strip(' ')
    assert source == data_source


# 用例35-【风险分析】验证访问用户IP页左侧的访问IP数据源不变但时间改变，是否显示最新的数据源
@then(parsers.cfparse("页面左侧最上方显示访问的数据源为[{data_source}]，访问时间为time1"),target_fixture="time1")
def step_impl(page, data_source):
    source = page.locator(locations_user["左侧-首个数据源"]).text_content().strip(' ')
    assert source == data_source
    time1 = page.locator(locations_user["左侧-首个数据源-访问时间"]).text_content().strip(' ')
    return time1


@given("已经等待5s")
def step_impl():
    time.sleep(5)


@when("再次进入风险分析-访问用户页面")
def step_impl(page):
    page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    page.locator("//div[@role='tablist']//div[text()='访问用户']").click()
    time.sleep(3)


@given("再次进入风险分析-访问用户页面")
def step_impl(page):
    page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    page.locator("//div[@role='tablist']//div[text()='访问用户']").click()
    time.sleep(1.2)
    time.sleep(1.5)


@then("访问时间time2大于time1")
def step_impl(page, time1):
    time2 = page.locator(locations_user["左侧-首个数据源-访问时间"]).text_content().strip(' ')
    difference = datetime.datetime.strptime(time2, '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(time1, '%Y-%m-%d %H:%M:%S')
    assert difference.seconds > 0


# 用例36-【风险分析】验证访问用户IP页左侧内容，时间是否倒序排列
@then("访问时间倒序排列")
def step_impl(page):
    count = page.locator(locations_user["左侧展开下拉列表"]).count()
    list_temp = []
    list_result = []
    if count > 10:
        count = 10
    for i in range(1, count+1):
        time1 = page.locator(locations_user["左侧-首个数据源-访问时间-按行"].format(str(i))).text_content().strip(' ')
        list_temp.append(time1)
    for i in range(len(list_temp)-1):
        difference = datetime.datetime.strptime(list_temp[i], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(list_temp[i+1], '%Y-%m-%d %H:%M:%S')
        list_result.append(difference.seconds)

    time.sleep(1.2)
    for j in list_result:
        assert j > 0


# 用例37-【风险分析】验证访问用户IP页的信息是否悬浮显示
@when("鼠标悬浮在访问用户IP时")
def step_impl(page):
    page.locator(locations_user["左侧-ip内容"]).hover()
    time.sleep(2)


@then('显示访问用户IP的访问分组信息:"访问分组"、"分组类别"、"客户端工具"、"数据库用户"')
def step_impl(page):
    base_loc = "//div[@role='tooltip' and @aria-hidden='false']/div/div"
    list1 = ["访问分组", "分组类别", "客户端工具", "数据库用户"]
    all_text = page.locator(base_loc).all_text_contents()
    list2 = []
    for tt in all_text:
        list2.append(tt.split('：')[0].strip(' '))

    assert list1 == list2


# 用例38-【风险分析】验证访问用户IP页的IP地址悬浮显示的字段位置和字段名称是否正确
@then('如果存在多个分组,多列用"|"分隔', target_fixture='dict_temp')
def step_impl(page):
    base_loc = "//div[@role='tooltip' and @aria-hidden='false']/div/div"
    all_text = page.locator(base_loc).all_text_contents()
    visit_group_list = all_text[0].split('：')[-1].strip(' ').split('|')
    group_type_list = all_text[1].split('：')[-1].strip(' ').split('|')
    dict_temp = dict(zip(visit_group_list, group_type_list))
    return dict_temp


@then("和该IP对应的访问分组和分组类别正确")
def step_impl(page, pages, dict_temp):
    base_loc = "//div[@class='main-table']//div[contains(@class,'el-table__body-wrapper')]//tbody//tr[1]//td[3]//div[@class='ellipsis el-popover__reference']"
    new_mask = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    for key in dict_temp.keys():
        new_mask.search_visit_group(key)
        time.sleep(0.2)
        content = page.locator(base_loc).text_content().strip(' ')
        assert content == dict_temp[key]


# 用例39-【风险分析】验证访问用户IP页的"显示用户"是否可点击
@given(parsers.cfparse("存在访问分组[{visit_group_name}]，且分组已开启身份认证"))
def step_impl(page, pages, visit_group_name):
    new_mask = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    new_mask.search_visit_group(visit_group_name)
    if new_mask.get_num() == 0:
        new_mask.new_visit_group(group_name=visit_group_name, need_login=True)


@when('点击用户IP右侧的"显示用户"时')
def step_impl(page):
    page.locator(locations_user["显示用户"]).click()
    time.sleep(1.2)


@then('"显示用户"切换为"不显示用户"')
def step_impl(page):
    expect(page.locator(locations_user["不显示用户"])).to_be_visible()


@when('点击用户IP右侧的"不显示用户"时')
def step_impl(page):
    page.locator(locations_user["不显示用户"]).click()
    time.sleep(1.2)


@then('"不显示用户"切换为"显示用户"')
def step_impl(page):
    expect(page.locator(locations_user["显示用户"])).to_be_visible()


# 用例40-【风险分析】验证访问用户IP页的"显示用户"是否可点击，并展示所有数据源
@when('点击用户IP右侧的"显示用户"')
def step_impl(page):
    page.locator(locations_user["显示用户"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


@when('点击访问用户ip左侧下拉')
def step_impl(page):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(2)


@when(parsers.cfparse("点击用户[{username}]左侧的展开按钮"))
def step_impl(page, username):
    page.locator(locations_user["用户左侧展开-按文本"].format(username)).click()
    time.sleep(1.2)


@then(parsers.cfparse("下方用户[{username}]访问过的数据源包含:[{data_source1}]和[{data_source2}]"))
def step_impl(page, username, data_source1, data_source2):
    data_list = page.locator(locations_user["数据源列表-按用户"].format(username)).all_text_contents()
    assert data_source1 in data_list
    assert data_source2 in data_list


# 用例41-【风险分析】验证访问用户IP页"所有会话"按钮右侧-帮助图标文案内容是否正确


@when('可以看到右侧的按钮："所有会话"')
def step_impl(page):
    expect(page.locator(locations_user["所有会话"])).to_be_visible()


@when("查看按钮右侧的问号图标")
def step_impl(page):
    page.locator(locations_user["所有会话-右侧问号"]).hover()
    time.sleep(0.5)


@then(parsers.cfparse('显示文本内容：[{content}]'))
def step_impl(page, content):
    real_content = page.locator(locations_user["所有会话-右侧hover弹框"]).text_content()
    assert content in real_content


# 用例42-【风险分析】验证访问用户IP页"所有会话"是否显示所有会话的信息
@when("展开访问用户ip，点击第一条数据源")
def step_impl(page):
    time.sleep(0.5)
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(2)
    page.locator(locations_user["左侧-首个数据源"]).click()
    time.sleep(3)
    # page.locator(locations_user["某行-sql语句点击"].format('1')).click()


@then("此时右侧数据SQL操作条数，成功条数，失败条数，高风险条数，脱敏操作条数分别为a,b,c,d,e", target_fixture="list_a")
def step_impl(page):
    list_a = []
    for i in range(1,6):
        content = page.locator(locations_user["风险统计条数-按列"].format(str(i))).text_content().strip(' ')
        list_a.append(content.split('：')[-1].replace('条', ''))
    return list_a


@when('点击"所有会话"')
def step_impl(page):
    page.locator(locations_user["所有会话"]).click()
    time.sleep(1.2)


@then("此时右侧SQL操作条数，成功条数，失败条数，高风险条数，脱敏操作条数分别为A,B,C,D,E", target_fixture="list_b")
def step_impl(page):
    list_b = []
    for i in range(1,6):
        content = page.locator(locations_user["风险统计条数-按列"].format(str(i))).text_content().strip(' ')
        list_b.append(content.split('：')[-1].replace('条', ''))
    return list_b


@then("数据a,b,c,d,e小于等于对应的A,B,C,D,E")
def step_impl(list_a, list_b):
    for i in range(len(list_a)):
        if list_a[i] != '':
            assert int(list_a[i]) <= int(list_b[i])


# 用例43-【风险分析】验证访问用户IP页会话语句，是否可点击并弹出SQL详情页
@when("点击会话编号下面展开的SQL语句时")
def step_impl(page):
    page.locator(locations_user["某行-sql语句点击"].format('1')).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then("语句可点击并正常弹出SQL详情")
def step_impl(page):
    loc = "//div[@class='rule-manager']"
    expect(page.locator(loc)).to_be_visible()


# 用例44-【风险分析】验证访问用户IP页的"持续时间"显示是否正常
@given(parsers.cfparse("运行中的脱敏任务[{task_name}]终止后再次重新启动"))
def step_impl(page, pages, task_name):
    new_task = MaskTaskPage(base_url=pages["task_info_page"], page=page)
    new_task.search(task_name)
    if page.locator(locations_mask_task["列表-首行-按钮-终止"]).is_visible():
        page.locator(locations_mask_task["列表-首行-按钮-终止"]).click()
        time.sleep(3)
        page.locator(locations_mask_task["列表-首行-按钮-启动"]).click()
        time.sleep(2)


@when(parsers.cfparse("选择第一个用户IP下的数据源[{conn_name}]"))
def step_impl(page, conn_name):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(2)
    page.locator('div .left >div .el-card__body>ul>li>div .el-popover__reference>div:has-text("{}")>>nth=0'.format(conn_name)).click()
    time.sleep(3)


@then("对应的持续时间显示该数据源被访问的开始时间和结束时间的区间")
def step_impl(page):
    time_text = page.locator(locations_user["持续时间"]).text_content().strip(' ')
    time_list = time_text.split('：')[-1].split(' - ')
    time_start = datetime.datetime.strptime(time_list[0].strip(' '), '%Y-%m-%d %H:%M:%S')
    time_end = datetime.datetime.strptime(time_list[1].strip(' '), '%Y-%m-%d %H:%M:%S')
    assert (time_end - time_start).seconds > 0


# 用例45-【风险分析】验证访问用户IP页的"会话编号"左侧展开收起正常
@when('点击右侧"会话编号"左侧的收起按钮')
def step_impl(page):
    page.locator(locations_user["右侧-会话展开收起"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


@then("sql语句展开收起正常")
def step_impl(page):
    expect(page.locator(locations_user["右侧-sql语句ul"])).not_to_be_visible()


@when('点击右侧"会话编号"左侧的展开按钮')
def step_impl(page):
    page.locator(locations_user["右侧-会话展开收起"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


@then("sql语句展开展开正常")
def step_impl(page):
    expect(page.locator(locations_user["右侧-sql语句ul"])).to_be_visible()


# 用例46-【风险分析】验证访问用户IP页的右侧下方查询条件字段显示、默认文本内容是否正确
@then('界面右侧下方的查询条件从左到右依次显示下拉框："会话编号"、"会话状态"')
def step_impl(page):
    expect(page.locator(locations_user["右侧-会话编号"])).to_be_visible()
    expect(page.locator(locations_user["右侧-会话状态"])).to_be_visible()


@then(parsers.cfparse('默认提示文本内容：[{msg}]'))
def step_impl(page, msg):
    content1 = page.locator(locations_user["右侧-会话编号"]).get_attribute('placeholder')
    content2 = page.locator(locations_user["右侧-会话状态"]).get_attribute('placeholder')
    assert msg == content1
    assert msg == content2


# 用例47-【风险分析】验证访问用户IP页的"会话状态"下拉框显示的枚举值是否正确
@when('点击"会话状态"下拉选项')
def step_impl(page):
    page.locator(locations_user["右侧-会话状态"]).click()
    time.sleep(1.2)
    time.sleep(0.5)


@then('可以看到枚举值从上到下分别显示"请求连接"、"连接中"、"断开"')
def step_impl(page):
    list1 = ["请求连接", "连接中", "断开"]
    all_text = page.locator(locations_user["右侧-会话状态-下拉列表"]).all_text_contents()
    assert list1 == all_text


# 用例48-【风险分析】验证访问用户IP页的"会话状态"下拉选择"请求连接"，是否可正常筛选出结果
@when('选择其中一个选项"断开"')
def step_impl(page):
    add_loc = "//span[text()='断开']"
    real_loc = locations_user["右侧-会话状态-下拉列表"] + add_loc
    page.locator(real_loc).click()
    time.sleep(1.2)
    time.sleep(0.2)


@then("筛选出的结果全部为断开连接状态的SQL语句")
def step_impl(page):
    all_text = page.locator(locations_user["右侧-左侧-所有会话状态"]).all_text_contents()
    for tt in all_text:
        assert tt == "断开"


# 用例49-【风险分析】验证访问用户IP页的"会话状态"下拉选择"连接中"，是否可正常筛选出结果
@given(data_table("存在脱敏任务代理端连接C，并执行以下sql访问, 保持连接状态", fixture="sql_list"),target_fixture="new_sql_conn")
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456', dbname='autotest1')
    for sql in sql_list:
        real_sql = sql["sql_command"]
        try:
            new_sql_conn.execute_sql(real_sql)
            time.sleep(0.2)
        except ConnectionError as e:
            logger.info("连接执行失败：{}".format(e.args))
        finally:
            logger.info("pass")
    time.sleep(2)
    return new_sql_conn


@when('右侧会话状态选择为"连接中"')
def step_impl(page):
    page.locator(locations_user["右侧-会话状态"]).click()
    time.sleep(1.2)
    add_loc = "//span[text()='连接中']"
    real_loc = locations_user["右侧-会话状态-下拉列表"] + add_loc
    page.locator(real_loc).click()
    time.sleep(1.2)
    time.sleep(0.5)


@then("筛选出的结果全部为连接中状态的SQL语句")
def step_impl(page):
    all_text = page.locator(locations_user["右侧-左侧-所有会话状态"]).all_text_contents()
    for tt in all_text:
        assert tt == "连接中"


@then("访问连接断开连接成功")
def step_impl(new_sql_conn):
    new_sql_conn.close()


# 用例50-【风险分析】访问用户IP页的右侧下方鼠标悬浮在每条SQL操作语句时，执行信息内容是否正确
@when("鼠标悬浮在第一条SQL操作语句时")
def step_impl(page):
    page.locator(locations_user["右侧-首条sql"]).hover()
    time.sleep(2)


@then('显示此条sql的执行信息内容正确,包括"执行结果"、"风险等级"、"安全操作"、"脱敏操作"',target_fixture="dict_temp")
def step_impl(page):
    all_text = page.locator(locations_user["右侧sql-hover文本弹框文本"]).all_text_contents()
    list1 = ["执行结果", "风险等级", "安全操作", "脱敏操作"]
    new_list = [i.split("：")[0] for i in all_text]
    assert list1 == new_list
    dict_temp = {}
    for tt in all_text:
        key = tt.split("：")[0]
        value = tt.split("：")[1]
        dict_temp[key] = value

    return dict_temp


@then("执行结果的枚举值包含：成功、失败")
def step_impl(dict_temp):
    assert dict_temp["执行结果"] in ["成功", "失败"]


@then("风险等级的枚举值包含：无风险、低风险、中风险、高风险、致命风险")
def step_impl(dict_temp):
    list1 = ['无风险', '低风险', '中风险', '高风险', '致命风险']
    assert dict_temp["风险等级"] in list1


@then("安全操作的枚举值包含：允许、放行、拦截、阻断、脱敏配置")
def step_impl(dict_temp):
    list1 = ['允许', '放行', '拦截', '阻断', '脱敏配置']
    assert dict_temp["安全操作"] in list1


@then("脱敏操作的枚举值包含：是、否")
def step_impl(dict_temp):
    assert dict_temp["脱敏操作"] in ['是', '否']


# 用例51-【风险分析】验证访问用户IP页的每个SQL语句右侧，执行耗时展示
@when("查看一个SQL语句右侧对应的耗时",target_fixture="list_time")
def step_impl(page):
    base_loc = "//div[@class='right']//div[@class='el-scrollbar__wrap']//ul//ul//li"
    count = page.locator(base_loc).count()
    list_time = []
    for i in range(1, count+1):
        tt = page.locator(locations_user["右侧-sql耗时-按行"].format(str(i))).text_content()
        list_time.append(tt)

    return list_time


@then('每个SQL语句右侧都显示"耗时(s)"，间隔0.005s')
def step_impl(list_time):
    for i in list_time:
        assert i[-1] == 's'
    for j in list_time:
        tt = j.replace('s','')
        a = int(float(tt)*1000)
        assert a%5 == 0


# 用例52-【风险分析】验证访问用户IP页的会话是否按操作时间进行倒序排列
@given(data_table("存在脱敏任务代理端连接C，并执行以下sql访问, 单条sql执行后，停留5s;", fixture="sql_list"))
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456',
                         dbname='autotest1')
    for sql in sql_list:
        real_sql = sql["sql_command"]
        try:
            new_sql_conn.execute_sql(real_sql)
            time.sleep(5)
        except ConnectionError as e:
            logger.info("连接执行失败：{}".format(e.args))
        finally:
            logger.info("pass")
    time.sleep(2)
    new_sql_conn.close()


@when("点击脱敏任务-对应的数据源[auto-mysql666]")
def step_impl(page):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_user["左侧-首个数据源"]).click()
    time.sleep(1.2)
    time.sleep(0.5)


@when("点击查看数据源对应的最新两次sql语句的访问时间")
def step_impl(page):
    page.locator(locations_user["右侧-首条sql"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    content1 = page.locator(locations_risk_detail["请求时间"]).text_content().strip(' ')
    time1 = datetime.datetime.strptime(content1, '%Y-%m-%d %H:%M:%S')

    page.locator("//button[@aria-label='close drawer']//i").click()
    time.sleep(1.2)
    page.locator(locations_user["右侧-sql-按行"].format('2')).click()
    time.sleep(1.2)
    content2 = page.locator(locations_risk_detail["请求时间"]).text_content().strip(' ')
    time2 = datetime.datetime.strptime(content2, '%Y-%m-%d %H:%M:%S')
    assert (time1-time2).seconds >= 5


@then("会话内的SQL语句按照执行的时间进行倒序排序")
def step_impl():
    pass
    # 上一步骤已验证


# 用例53-【风险分析】访问用户IP页的持续时间显示数据是否正确-有正在进行的操作
@given(data_table("存在脱敏任务代理端连接B，并执行以下sql访问，保持连接状态", fixture="sql_list"), target_fixture="new_sql_conn")
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456',
                         dbname='autotest1')
    for sql in sql_list:
        real_sql = sql["sql_command"]
        try:
            new_sql_conn.execute_sql(real_sql)
            time.sleep(2)
        except ConnectionError as e:
            logger.info("连接执行失败：{}".format(e.args))
        finally:
            logger.info("pass")
    time.sleep(2)
    return new_sql_conn


@when(parsers.cfparse("风险分析选择数据源[{conn_name}]"))
def step_impl(page, conn_name):
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    page.locator(locations_user["左侧-数据源按文本-可能多个"].format(conn_name)).first.click()
    time.sleep(1.2)
    time.sleep(0.5)


@when('查看"持续时间"数据时',target_fixture="continue_time")
def step_impl(page):
    continue_time = page.locator(locations_user["持续时间"]).text_content().strip(' ')
    return continue_time


@then('显示的是："开始时间-"')
def step_impl(page, continue_time):
    time_list = continue_time.split(' - ')
    assert len(time_list) == 1
    assert time_list[0] != ''


# 用例54-【风险分析】访问用户IP页的左侧显示内容，是否是查询条件"访问IP"、"时间范围"筛选后的结果
@when('"时间范围"输入数据为今天到明天')
def step_impl(page):
    today1 = str(datetime.datetime.today()).split('.')[0]
    tomorrow = str(datetime.datetime.today() + datetime.timedelta(days=1)).split('.')[0]
    page.locator(locations_user["查询-时间范围-开始"]).fill(today1)
    page.locator(locations_user["查询-时间范围-结束"]).fill(tomorrow)


@when("点击风险分析-访问用户-查询按钮")
def step_impl(page):
    page.locator(locations_user["查询按钮"]).click()
    time.sleep(1.2)


@then('页面左侧展示数据源"时间范围"在今天')
def step_impl(page):
    today_now = str(datetime.date.today())
    page.locator(locations_user["左侧展开收起图标"]).click()
    time.sleep(1.2)
    time.sleep(1.2)
    count = page.locator(locations_user["左侧展开下拉列表"]).count()
    list_temp = []
    if count > 10:
        count = 10
    for i in range(1, count + 1):
        time1 = page.locator(locations_user["左侧-首个数据源-访问时间-按行"].format(str(i))).text_content().strip(' ')
        list_temp.append(time1)

    time.sleep(1.2)
    for j in list_temp:
        time_t = j.split(' ')[0]
        assert time_t == today_now


# 用例55-验证数据源页面的页面布局是否正常
@given('已经进入到风险分析-数据源页签')
def step_impl(page):
    page.locator("//li[@role='menuitem']//span[text()='风险分析']").click()
    time.sleep(1.2)
    page.locator("//div[@role='tablist']//div[text()='数据源']").click()
    time.sleep(5)


@then("左侧板块显示系统存在数据源")
def step_impl(page):
    time.sleep(0.5)
    count = page.locator(locations_data_source["左侧-数据源卡片-多个"]).count()
    assert count > 0


@then('数据源上方显示筛选条件："数据源名称"')
def step_impl(page):
    expect(page.locator(locations_data_source["左侧-数据源输入框"])).to_be_visible()


@then('右侧上部板块显示默认查询条件"显示频率"、"时间范围"')
def step_impl(page):
    expect(page.locator(locations_data_source["显示频率"])).to_be_visible()
    expect(page.locator(locations_data_source["时间范围-开始"])).to_be_visible()
    expect(page.locator(locations_data_source["时间范围-结束"])).to_be_visible()


@then('右侧中部显示查询条件为"会话状态"、"安全操作"、"风险等级"、"执行结果"，按钮依次显示："重置"、"查询"')
def step_impl(page):
    for loc in ["会话状态", "安全操作", "风险等级", "执行结果", "重置按钮", "查询按钮"]:
        expect(page.locator(locations_data_source[loc])).to_be_visible()


@then('右侧中部显示列表字段为"访问用户IP","任务名称","会话编号","会话状态","SQL编号","SQL语句","风险等级","执行结果","安全操作"')
def step_impl(page):
    list1 = ["访问用户IP", "任务名称", "会话编号", "会话状态", "SQL编号", "SQL语句", "风险等级", "执行结果", "安全操作"]
    all_text = page.locator(locations_data_source["列表-表头-多字段"]).all_text_contents()
    for name in list1:
        assert name in all_text


@then('板块2页面最下方左侧置灰显示为"双击单条数据可查看SQL语句详情"，在右侧显示为分页器包含"共 页","前往1页"')
def step_impl(page):
    loc1 = "//p[@class='primary tip' and text()='提示：双击单条数据可查看SQL语句详情']"
    loc2 = "//span[@class='el-pagination__total' and contains(text(),'共') and contains(text(),'条')]"
    loc3 = "//span[@class='el-pagination__jump' and contains(text(),'前往')]"
    loc4 = "//span[@class='el-pagination__jump']//input"
    for loc in [loc1, loc2, loc3]:
        expect(page.locator(loc)).to_be_visible()
    assert page.locator(loc4).input_value() == '1'


# 用例56-验证点击数据源页签后，是否正确显示数据源个数
@when("数据源页面中存在多个数据源",target_fixture="count")
def step_impl(page):
    count = page.locator(locations_data_source["左侧-数据源卡片-多个"]).count()
    assert count > 0
    return count


@then('数据源页签显示:"数据源(3)"')
def step_impl(page, count):
    loc = "//div[@role='tablist']//div[@id='tab--3']"
    content = page.locator(loc).text_content().strip(' ')
    exp_str = '数据源({})'.format(str(count))
    assert content == exp_str


# 用例57-验证数据源页面，"数据源名称"右侧的数据源是否可点击弹出数据源详情
@when(parsers.cfparse('数据源名称下拉选择[{conn_name}]'))
def step_impl(page, conn_name):
    page.locator(locations_data_source["左侧-数据源输入框"]).click()
    time.sleep(1.2)
    page.locator(locations_data_source["左侧-数据源下拉点击-按名称"].format(conn_name)).click()
    time.sleep(3.2)


@when('点击首个数据源的"数据源名称"时')
def step_impl(page):
    page.locator(locations_data_source["左侧-数据源名称-可能多个"]).first.click()
    time.sleep(1.2)
    time.sleep(0.5)


@then("弹出数据源详情")
def step_impl(page):
    loc = "//div[@class='el-dialog__wrapper' and not(contains(@style,'none'))]//span[@class='el-dialog__title']"
    expect(page.locator(loc)).to_be_visible()


# 用例58-验证数据源页面，查询条件"数据源名称"是否可下拉选择
@when('下拉点击查询条件中的"数据源名称"')
def step_impl(page):
    page.locator(locations_data_source["左侧-数据源输入框"]).click()
    time.sleep(1.2)


@then(parsers.cfparse("下拉选择列表可以看到[{conn_name}]"))
def step_impl(page, conn_name):
    expect(page.locator(locations_data_source["左侧-数据源下拉点击-按名称"].format(conn_name))).to_be_visible()


# 用例59-验证数据源页面，查询条件"数据源名称"下拉选择后的筛选结果是否正确
@then(parsers.cfparse("左侧数据源仅可以看到[{conn_name}]"))
def step_impl(page, conn_name):
    count = page.locator(locations_data_source["左侧-数据源卡片-多个"]).count()
    assert count == 1
    name1 = page.locator(locations_data_source["左侧-数据源名称-可能多个"]).text_content().strip(' ')
    assert name1 == conn_name


# 用例60-验证数据源页面，每个数据源卡片内显示字段是否正确
@then('数据源名称下部左侧显示字段:"SQL语句(条)"、"风险语句(条）"、"访问用户IP(个)"')
def step_impl(page):
    base_loc = locations_data_source["左侧-数据源卡片-首个"]
    name_list = ["左侧-sql语句条数", "左侧-风险语句条数", "左侧-访问用户ip条数"]
    for name in name_list:
        new_loc = base_loc + locations_data_source[name]
        expect(page.locator(new_loc)).to_be_visible()


@then('右侧显示每个字段对应的"当前/全部"对应的数值')
def step_impl(page):
    base_loc = "//div[@class='resource-container']//div[@class='left']//div[@class='el-card box-card is-always-shadow'][1]//span[text()='当前/全部']"
    expect(page.locator(base_loc)).to_be_visible()


# 用例61-验证数据源页面，每个数据源卡片内的"访问用户IP(个)"是否可展开
@when('展开数据源卡片内的"访问用户IP(个)"')
def step_impl(page):
    page.locator(locations_data_source["访问用户ip-左侧展开"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then("可以看到对应的访问ip地址")
def step_impl(page):
    expect(page.locator(locations_data_source["左侧-ip地址-单个"])).to_be_visible()


@when("鼠标点击ip左侧的展开按钮")
def step_impl(page):
    page.locator(locations_data_source["左侧-ip左侧展开"]).click()
    time.sleep(2)


@then("ip展开正常")
def step_impl(page):
    expect(page.locator(locations_data_source["左侧-ip展开-用户名"])).to_be_visible()


# 用例62-验证数据源页面，每个数据源卡片内的"访问用户IP(个)"是否显示用户IP以及IP用户
@then(parsers.cfparse("正常展示访问ip的用户[{username}]"))
def step_impl(page, username):
    user = page.locator(locations_data_source["左侧-ip展开-用户名"]).text_content().strip(' ')
    assert user == username


# 用例63-验证数据源页面，数据源卡片查询组件能否进行查询
@when("查看数据源卡片时")
def step_impl():
    pass


# 用例64-验证数据源页面，查看风险分布页面显示频率下拉是否可选"分钟"、"小时"、"天"
@when("查看风险分布曲线部分")
def step_impl():
    pass


@when("点击显示频率下拉框")
def step_impl(page):
    page.locator(locations_data_source["显示频率"]).click()
    time.sleep(1.2)


@then('显示可下拉选择"分钟"、"小时"、"天"')
def step_impl(page):
    list1 = ["分钟", "小时", "天"]
    for name in list1:
        new_loc = locations_data_source["下拉列表选择"].format(name)
        expect(page.locator(new_loc)).to_be_visible()


# 用例65-验证数据源页面,当存在执行失败SQL操作语句时，鼠标悬浮是否可查看失败原因
@when('点击数据源"访问用户IP(个)"')
def step_impl(page):
    page.locator(locations_data_source["左侧-访问用户IP(个)"]).click()
    time.sleep(1.2)


@when(parsers.cfparse("会话列表查询选择-执行结果为[{result}]的会话"))
def step_impl(page, result):
    page.locator(locations_data_source["执行结果"]).click()
    time.sleep(1.2)
    page.locator(locations_data_source["下拉列表选择"].format(result)).click()
    time.sleep(1.2)
    page.locator(locations_data_source["查询按钮"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@when('操作鼠标放置首行"执行结果"为"失败"的图标"!"上时')
def step_impl(page):
    page.locator(locations_data_source["列表-首行-执行结果-失败图标"]).hover()
    time.sleep(0.5)


@then(parsers.cfparse("悬浮显示具体失败的原因[{reason}]"))
def step_impl(page, reason):
    msg_list = reason.split('|')
    content = page.locator(locations_data_source["列表-失败原因hover"]).text_content().strip(' ')
    assert content in msg_list


# 用例66-验证数据源页面列表下方提示信息是否展示正确
@then(parsers.cfparse("访问数据列表下方提示信息展示：[{msg}]"))
def step_impl(page, msg):
    content = page.locator(locations_data_source["列表下方提示"]).text_content().strip(' ')
    assert content == msg


# 用例67-验证数据源页面,列表下方双击单条数据是否可查看SQL语句详情
@given('系统中已存在多行"访问用户IP"对应列表数据')
def step_impl(page):
    count = page.locator(locations_data_source["列表-当前行数"]).count()
    assert count > 1


@when('双击首行"访问用户IP"对应数据时')
def step_impl(page):
    page.locator(locations_data_source["列表-某行-sql语句"].format('1')).dblclick()


@then("页面右侧弹出SQL语句详情页面")
def step_impl(page):
    expect(page.locator("//div[@class='rule-manager']")).to_be_visible()
    time.sleep(0.2)


# 用例68-验证数据源页面,SQL语句详情页面显示是否正常
@when('点击首行"SQL编号"时')
def step_impl(page):
    page.locator(locations_data_source["列表-首行-sql编号"]).click()
    time.sleep(1.2)


# 用例69-验证数据源页面会话状态下拉枚举值是否正确
@when('下拉查看列表查询条件中的"会话状态"')
def step_impl(page):
    page.locator(locations_data_source["会话状态"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then('枚举值依次显示:"请求连接"、"连接中"、"断开"')
def step_impl(page):
    list1 = ["请求连接", "连接中", "断开"]
    all_text = page.locator(locations_data_source["下拉列表多个"]).all_text_contents()
    assert all_text == list1


# 用例70-验证数据源页面安全操作下拉枚举值是否正确
@when("查看下方会话列表部分")
def step_impl():
    pass


@when('下拉查看查询条件中的"安全操作"')
def step_impl(page):
    page.locator(locations_data_source["安全操作"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then('枚举值依次显示:"拦截"、"终止"、"放行"')
def step_impl(page):
    list1 = ["拦截", "终止", "放行"]
    all_text = page.locator(locations_data_source["下拉列表多个"]).all_text_contents()
    assert all_text == list1


# 用例71-验证数据源页面风险等级下拉枚举值是否正确
@when('下拉查看查询条件中的"风险等级"')
def step_impl(page):
    page.locator(locations_data_source["风险等级"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then('枚举值依次显示:"无"、"低"、"中"、"高"')
def step_impl(page):
    list1 = ["无", "低", "中", "高"]
    all_text = page.locator(locations_data_source["下拉列表多个"]).all_text_contents()
    assert all_text == list1


# 用例72-验证数据源页面执行结果下拉枚举值是否正确
@when('下拉查看查询条件中的"执行结果"')
def step_impl(page):
    page.locator(locations_data_source["执行结果"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then('枚举值依次显示:"失败"、"成功"')
def step_impl(page):
    list1 = ["失败", "成功"]
    all_text = page.locator(locations_data_source["下拉列表多个"]).all_text_contents()
    assert all_text == list1


# 用例73-验证数据源页面，组合查询是否成功
@when(parsers.parse('依次下拉选择"会话状态"{dialogue_state}，"安全操作"{safety_operation}，"风险等级"{risk_level}，"执行结果"{execution_result}'),target_fixture="result_list")
def step_impl(page, dialogue_state, safety_operation, risk_level, execution_result):
    time.sleep(1)
    if dialogue_state not in ['null', 'NULL', '']:
        page.locator(locations_data_source["会话状态"]).click()
        time.sleep(1.2)
        page.locator(locations_data_source["下拉列表选择"].format(dialogue_state)).click()
        time.sleep(1.2)
    if safety_operation not in ['null', 'NULL', '']:
        page.locator(locations_data_source["安全操作"]).click()
        time.sleep(1.2)
        page.locator(locations_data_source["下拉列表选择"].format(safety_operation)).click()
        time.sleep(1.2)
    if risk_level not in ['null', 'NULL', '']:
        page.locator(locations_data_source["风险等级"]).click()
        time.sleep(1.2)
        page.locator(locations_data_source["下拉列表选择"].format(risk_level)).click()
        time.sleep(1.2)
    if execution_result not in ['null', 'NULL', '']:
        page.locator(locations_data_source["执行结果"]).click()
        time.sleep(1.2)
        page.locator(locations_data_source["下拉列表选择"].format(execution_result)).click()
        time.sleep(1.2)
    result_list = [dialogue_state, safety_operation, risk_level, execution_result]
    return result_list


@when('点击风险分析-数据源页-列表"查询"')
def step_impl(page):
    time.sleep(1.2)
    page.locator(locations_data_source["查询按钮"]).click()
    time.sleep(3)


@then("页面应该显示符合查询条件的数据")
def step_impl(page, result_list):
    lines = page.locator(locations_data_source["列表-当前行数"]).count()
    for line in range(1, lines+1):
        tt1 = page.locator(locations_data_source["某行-连接状态"].format(str(line))).text_content().strip(' ')
        tt2 = page.locator(locations_data_source["某行-安全操作"].format(str(line))).text_content().strip(' ')
        tt3 = page.locator(locations_data_source["某行-风险等级"].format(str(line))).text_content().strip(' ')
        tt4 = page.locator(locations_data_source["某行-执行结果"].format(str(line))).text_content().strip(' ')[:2]
        list_temp = [tt1, tt2, tt3, tt4]
        assert list_temp == result_list


# 用例74-验证数据源页面，单个查询是否成功
@then("页面应该显示符合查询条件的数据1")
def step_impl(page, result_list):
    list1 = ['某行-连接状态', '某行-安全操作', '某行-风险等级', '某行-执行结果']
    dict_temp = dict(zip(result_list, list1))
    lines = page.locator(locations_data_source["列表-当前行数"]).count()
    for key in result_list:
        if key != 'null':
            for line in range(1, lines + 1):
                tt = page.locator(locations_data_source[dict_temp[key]].format(str(line))).text_content().strip(' ')
                assert tt == key


# 用例75-验证数据源页面，重置功能是否正常
@when(parsers.cfparse('下拉选择"会话状态"-[{choice}]'))
def step_impl(page, choice):
    page.locator(locations_data_source["会话状态"]).click()
    time.sleep(1.2)
    page.locator(locations_data_source["下拉列表选择"].format(choice)).click()
    time.sleep(1.2)
    time.sleep(1.2)
    content = page.locator(locations_data_source["会话状态"]).input_value()
    assert content != ''


@when('点击风险分析-数据源查询"重置"')
def step_impl(page):
    page.locator(locations_data_source["重置按钮"]).click()
    time.sleep(1.2)


@then("会话状态查询条件清空")
def step_impl(page):
    content = page.locator(locations_data_source["会话状态"]).input_value()
    assert content == ""


# 用例76-验证数据源页面，鼠标点击SQL语句详情页面外的区域时，是否可关闭SQL语句详情页面
@when("操作鼠标点击SQL语句详情页面外的区域时")
def step_impl(page):
    # loc1 = "//div[contains(text(),'数据源名称：')]"
    loc1 = "//div[@role='document']"
    page.locator(loc1).highlight()
    time.sleep(2)
    page.locator(loc1).click()
    time.sleep(1.2)


@then("SQL语句详情页面关闭，并返回至风险分析页面数据源页签")
def step_impl(page):
    loc1 = "//div[contains(text(),'数据源名称：')]"
    expect(page.locator("//div[@class='rule-manager']")).not_to_be_visible()
    expect(page.locator(loc1)).to_be_visible()


# 用例77-验证数据源页面，点击"X"是否可关闭SQL语句详情页面
@when('点击SQL语句详情页右上角"X"时')
def step_impl(page):
    loc = "//button[@aria-label='close drawer']/i"
    page.locator(loc).click()
    time.sleep(1.2)


# 用例78-验证自定义页签的"＋新增"，是否可点击并正常弹窗
@when('点击"新增"页签')
def step_impl(page):
    page.locator(locations_general["新增页签按钮"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


@then("可以正常弹出自定义页签的新增窗口")
def step_impl(page):
    expect(page.locator(locations_general["页签新增title"])).to_be_visible()


# 用例79-验证自定义页签弹窗的页面元素是否正常展示
@then('新增窗口显示"新增"标题')
def step_impl(page):
    expect(page.locator(locations_general["页签新增title"])).to_be_visible()


@then('从上到下依次显示字段名称:"页签名称"、"页面显示"、"筛选条件"')
def step_impl(page):
    expect(page.locator(locations_general["页签新增-页签名称-字段"])).to_be_visible()
    expect(page.locator(locations_general["页签新增-页面显示-字段"])).to_be_visible()
    expect(page.locator(locations_general["页签新增-筛选条件-字段"])).to_be_visible()


@then('页面显示字段下拉枚举值包含:"全局信息"、"访问用户"、"数据源"')
def step_impl(page):
    page.locator(locations_general["页签新增-页面显示"]).click()
    time.sleep(1.2)
    for name in ["全局信息", "访问用户", "数据源"]:
        new_loc = locations_general["页签新增-下拉选择-按文本"].format(name)
        expect(page.locator(new_loc)).to_be_visible()


@then('包含两个按钮，从左到右依次显示:"取消"、"保存"')
def step_impl(page):
    expect(page.locator(locations_general["页签新增-取消按钮"])).to_be_visible()
    expect(page.locator(locations_general["页签新增-保存按钮"])).to_be_visible()


# 用例80-验证自定义页签-弹窗内容所有内容是否必填
@when("查看弹窗内容时")
def step_impl():
    pass


@then(parsers.cfparse('"页面显示"默认显示的是[{text1}]'))
def step_impl(page, text1):
    content = page.locator(locations_general["页签新增-页面显示"]).input_value()
    assert content == text1


# 用例81-验证自定义页签，"页面显示"选择"全局信息"，能否新增成功
@when(parsers.parse('新增窗口输入"页签名称"{tag_name}、"页面显示"{page_display}、筛选条件：访问分组{access_group}、SQL功能类型{sql_type}、脱敏操作{mask_operation}'))
def step_impl(page, tag_name, page_display, access_group, sql_type, mask_operation):
    page.locator(locations_general["页签新增-页签名称"]).fill(tag_name)
    if page_display != "全局信息":
        page.locator(locations_general["页签新增-页面显示"]).click()
        time.sleep(1.2)
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(page_display)).click()
        time.sleep(1.2)
    page.locator(locations_general["页签新增-筛选条件"]).click()
    time.sleep(1.2)
    time.sleep(0.5)
    for tt in ['访问分组', 'SQL功能类型', '脱敏操作']:
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(tt)).click()
        time.sleep(2.2)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)
    list1 = ['访问分组', 'SQL功能类型', '脱敏操作']
    # list1 = ['访问分组', '脱敏操作']
    list2 = [access_group, sql_type, mask_operation]
    dict_temp = dict(zip(list1, list2))
    for key in list1:
        page.locator(locations_general["页签新增-筛选条件-输入框-展开按钮"].format(key)).click()
        time.sleep(1.2)
        time.sleep(0.2)
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(dict_temp[key])).click()
        time.sleep(1.2)
        time.sleep(0.5)
        page.locator(locations_general["页签新增title"]).click()
        time.sleep(1.2)


@when("点击页签新增保存")
def step_impl(page):
    page.locator(locations_general["页签新增-保存按钮"]).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then(parsers.parse("页签新增成功，风险分析页签多了一个新增页签，名称和设置的名称{tag_name}保持一致"))
def step_impl(page, tag_name):
    tag_loc = locations_general["顶部页签-按名称"].format(tag_name)
    expect(page.locator(tag_loc)).to_be_visible()


@when(parsers.parse('点击自定义的页签{tag_name}名称后的"X"'), target_fixture="tag_name")
def step_impl(page, tag_name):
    page.locator(locations_general["页签删除-按文本"].format(tag_name)).click()
    time.sleep(1.2)
    time.sleep(1.2)
    return tag_name


# 用例82-验证自定义页签，"页面显示"选择"访问用户"，能否新增成功
@when(parsers.parse('新增窗口输入"页签名称"{tag_name}、"页面显示"{page_display}、选择访问时间-"开始时间"{start_time}、"结束时间"{end_time}、"访问用户IP"{user_ip}'))
def step_impl(page, tag_name, page_display, start_time, end_time, user_ip):
    page.locator(locations_general["页签新增-页签名称"]).fill(tag_name)
    if page_display != "全局信息":
        page.locator(locations_general["页签新增-页面显示"]).click()
        time.sleep(1.2)
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(page_display)).click()
        time.sleep(1.2)
    page.locator(locations_general["页签新增-筛选条件"]).click()
    time.sleep(1.2)
    for tt in ['访问时间', '访问用户IP']:
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(tt)).click()
        time.sleep(1.2)
    time.sleep(1.2)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)
    page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('访问用户IP')).fill(user_ip)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)
    time.sleep(0.2)
    page.locator("//div[@aria-label='新增']//input[@placeholder='开始日期']").fill(start_time)
    page.locator("//div[@aria-label='新增']//input[@placeholder='结束日期']").fill(start_time)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)
    time.sleep(0.2)


# 用例83-验证自定义页签，"页面显示"选择"数据源"，能否新增成功
@when(parsers.parse('新增窗口输入"页签名称"{tag_name}、"页面显示"{page_display}、"筛选条件:数据源"{data_source}、"筛选条件:访问用户IP"{user_ip}'))
def step_impl(page, tag_name, page_display, data_source, user_ip):
    page.locator(locations_general["页签新增-页签名称"]).fill(tag_name)
    if page_display != "全局信息":
        page.locator(locations_general["页签新增-页面显示"]).click()
        time.sleep(1.2)
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(page_display)).click()
        time.sleep(1.2)
    page.locator(locations_general["页签新增-筛选条件"]).click()
    time.sleep(1.2)
    time.sleep(0.2)
    for tt in ['数据源', '访问用户IP']:
        page.locator(locations_general["页签新增-下拉选择-按文本"].format(tt)).click()
        time.sleep(1.2)
    time.sleep(1.2)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)
    page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('访问用户IP')).fill(user_ip)
    time.sleep(0.2)
    page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('数据源')).fill(data_source)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)


# 用例84-验证自定义页签，能否取消成功
@when(parsers.cfparse('新增窗口输入"页签名称"输入[{tag_name}]、"页面显示"默认"全局信息"、"筛选条件"下拉选择"数据源"'))
def step_impl(page, tag_name):
    page.locator(locations_general["页签新增-页签名称"]).fill(tag_name)
    page.locator(locations_general["页签新增-筛选条件"]).click()
    time.sleep(1.2)
    time.sleep(0.2)
    page.locator(locations_general["页签新增-下拉选择-按文本"].format('数据源')).click()
    time.sleep(1.2)
    time.sleep(0.2)
    page.locator(locations_general["页签新增title"]).click()
    time.sleep(1.2)


@when(parsers.cfparse("筛选条件数据源输入[{data_source}]"))
def step_impl(page, data_source):
    page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('数据源')).fill(data_source)


@when('点击页签新增"取消按钮"')
def step_impl(page):
    page.locator(locations_general["页签新增-取消按钮"]).click()
    time.sleep(1.2)


@then("页签新增弹窗消失")
def step_impl(page):
    expect(page.locator(locations_general["页签新增title"])).not_to_be_visible()


# 用例85-验证自定义页签，能否删除成功
@given(parsers.cfparse('点击"新增"页签[{tag_name}]并新增成功'))
def step_impl(page, pages, tag_name):
    new_analysis = RiskAnalysisPage(base_url=pages['risk_analysis_page'], page=page)
    new_analysis.new_tag(tag_name=tag_name, data_source='test111')
    time.sleep(1.2)


@when(parsers.cfparse('点击自定义页签[{tag_name}]名称后的"X"'), target_fixture="tag_name")
def step_impl(page, tag_name):
    page.locator(locations_general["页签删除-按文本"].format(tag_name)).click()
    time.sleep(1.2)
    time.sleep(0.5)
    return tag_name


@when('点击页签删除"确定"按钮')
def step_impl(page):
    page.locator(locations_general["页签删除提醒-确定"]).click()
    time.sleep(1.2)
    time.sleep(0.5)


@then("页签删除成功")
def step_impl(page, tag_name):
    expect(page.locator(locations_general["顶部页签-按名称"].format(tag_name))).not_to_be_visible()


# 用例86-验证自定义页签，删除提示信息是否正确
@then(parsers.cfparse('弹出提示窗口：[{msg}]'))
def step_impl(page, msg):
    content = page.locator(locations_general["删除提示内容"]).text_content()
    assert content == msg


@then(parsers.cfparse('页签删除提示:[{msg}]'))
def step_impl(page, msg):
    base_loc = "//div[@role='alert']//p[text()='{}']"
    new_loc = base_loc.format(msg)
    expect(page.locator(new_loc)).to_be_visible()


# 用例87-验证自定义页签，筛选条件选择后能否删除成功
@when('筛选条件选择"数据源"')
def step_impl(page):
    page.locator(locations_general["页签新增-筛选条件"]).click()
    time.sleep(1.2)
    page.locator(locations_general["页签新增-下拉选择-按文本"].format('数据源')).click()
    time.sleep(1.2)


@then('筛选条件下面增加一行必填项："数据源"')
def step_impl(page):
    expect(page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('数据源'))).to_be_visible()


@when('点击筛选条件中数据源后面的"X"或筛选条件下的数据源文本框右侧的"X"')
def step_impl(page):
    page.locator(locations_general["数据源右侧-删除"]).click()
    time.sleep(1.2)


@then('"数据源"筛选条件被删除')
def step_impl(page):
    expect(page.locator(locations_general["页签新增-筛选条件-输入框-按文本"].format('数据源'))).not_to_be_visible()


# 用例88-验证自定义页签-新建成功的页签，每次进入是否为设置的筛选条件且数据展示正确
@when(parsers.cfparse("翻到其他页面再重新进入[{tag_name}]页签时"))
def step_impl(page, pages, tag_name):
    page.goto(pages["connection_page"])
    time.sleep(2)
    page.go_back()
    page.locator(locations_general["顶部页签-按名称"].format(tag_name)).click()
    time.sleep(1.2)


@then("左上方筛选条件仅展示[数据源]")
def step_impl(page):
    loc1 = "//label[@for='resourceName']"
    loc2 = "//div[@class='search-form-item']//label"
    expect(page.locator(loc1)).to_be_visible()
    assert page.locator(loc2).count() == 1


@then(parsers.cfparse("数据源内默认筛选值为[{value}]"))
def step_impl(page, value):
    base_loc = "//div[@class='search-form-item']//label[@for='resourceName']/following-sibling::div//input"
    content = page.locator(base_loc).input_value()
    assert content == value


# 用例89-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"显示内容是否正确
@when(parsers.cfparse("输入sql语句[{sql_command}]并查询"))
def step_impl(page, sql_command):
    loc = locations_search["搜索框-输入-按文本"].format('SQL语句')
    page.locator(loc).fill(sql_command)
    page.locator(locations_search["查询按钮"]).click()
    time.sleep(1.2)
    time.sleep(0.5)


@then(parsers.cfparse("SQL详情页-安全防护,SQL操作内容为[{content}]"),target_fixture="dict_temp")
def step_impl(page, content):
    list1 = ['SQL操作', '命中规则', '规则风险', '安全操作', '脱敏操作', '脱敏方案']
    dict_temp = {}
    for key in list1:
        value = page.locator(locations_risk_detail["详情页-通用文本"].format(key)).text_content().strip(' ')
        dict_temp[key] = value

    assert dict_temp["SQL操作"] == content
    return dict_temp


@then(parsers.cfparse("SQL详情页-安全防护,[{key}]内容为[{value}]"))
def step_impl(dict_temp, key, value):
    if value == 'null':
        assert dict_temp[key] == ''
    else:
        assert dict_temp[key] == value


# 用例90-验证"访问用户"页存在SQL语句，SQL详情页的字段内容是否正确
@then(parsers.cfparse("SQL详情页-安全防护-首行数据展示-字段名称[{text1}]，脱敏方式[{text2}]，数据集[{text3}]"))
def step_impl(page, text1, text2, text3):
    list1 = [text1, text2, text3]
    tt1 = page.locator(locations_risk_detail["右侧-某行-字段名"].format('1')).text_content().strip(' ')
    tt2 = page.locator(locations_risk_detail["右侧-某行-脱敏方式"].format('1')).text_content().strip(' ')
    tt3 = page.locator(locations_risk_detail["右侧-某行-数据集-首个"].format('1')).text_content().strip(' ')
    list2 = [tt1, tt2, tt3]
    assert list1 == list2


@then(parsers.cfparse("SQL详情页-安全防护-第二行数据展示-字段名称[{text1}]，脱敏方式[{text2}]，数据集[{text3}]"))
def step_impl(page, text1, text2, text3):
    list1 = [text1, text2, text3]
    tt1 = page.locator(locations_risk_detail["右侧-某行-字段名"].format('2')).text_content().strip(' ')
    tt2 = page.locator(locations_risk_detail["右侧-某行-脱敏方式"].format('2')).text_content().strip(' ')
    tt3 = page.locator(locations_risk_detail["右侧-某行-数据集-首个"].format('2')).text_content().strip(' ')
    list2 = [tt1, tt2, tt3]
    assert list1 == list2


# 用例91-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"字段下方的"查看更多"是否可点击并弹窗
@when('点击SQL详情页-安全防护-下方"查看更多"按钮')
def step_impl(page):
    page.locator(locations_risk_detail['查看更多']).click()
    time.sleep(1.2)
    time.sleep(1.2)


@then('正常弹出"脱敏数据详情"页')
def step_impl(page):
    base_loc = "//span[@class='el-dialog__title' and text()='脱敏数据详情']"
    expect(page.locator(base_loc)).to_be_visible()


@then("分页每页默认10行")
def step_impl(page):
    base_loc = "//div[@aria-label='脱敏数据详情']//span[@class='el-pagination__sizes']//input"
    content = page.locator(base_loc).input_value()
    assert content == "10条/页"


# 用例92-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"字段下方的"查看更多"显示字段内容是否正确
@then(parsers.cfparse("详情页字段名包括[{columns}]"))
def step_impl(page, columns):
    column_list = columns.split(',')
    all_text = page.locator(locations_risk_detail["脱敏数据详情-表头"]).all_text_contents()
    for i in column_list:
        assert i in all_text


@then(parsers.cfparse("第三个字段包含内容：[{values}]"))
def step_impl(page, values):
    value_list = values.split(',')
    all_text = page.locator(locations_risk_detail["脱敏数据详情-某行多列文本"].format('3')).all_text_contents()
    assert value_list == all_text


@then(parsers.cfparse("第四个字段包含内容：[{values}]"))
def step_impl(page, values):
    value_list = values.split(',')
    all_text = page.locator(locations_risk_detail["脱敏数据详情-某行多列文本"].format('4')).all_text_contents()
    assert value_list == all_text


# 用例93-【风险分析】验证访问用户IP页从其他界面切入，SQL操作小于20条时，默认展示是否正确一致
@then("SQL操作条数 和 会话下方sql语句条数 一致")
def step_impl(page):
    time.sleep(2)
    content = page.locator(locations_user["sql操作条数"]).text_content().strip(' ')
    a = content.split('：')[-1][:-1]
    if a == '':
        num1 = 0
    else:
        num1 = int(content.split('：')[-1][:-1])
    num2 = page.locator(locations_user["右侧-sql条数"]).count()
    if num1 <= 20:
        assert int(num1) == num2
    else:
        assert int(num1) > num2

# 用例94-【风险分析】验证访问用户IP页从其他界面切入，SQL操作大于20条时，默认展示是否正确
@given(data_table("存在脱敏任务代理端连接B，并执行以下sql访问--循环执行22次",fixture='sql_list'))
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456',
                         dbname='autotest1')
    for i in range(22):
        for sql in sql_list:
            real_sql = sql["sql_command"]
            try:
                new_sql_conn.execute_sql(real_sql)
                time.sleep(0.2)
            except ConnectionError as e:
                logger.info("连接执行失败：{}".format(e.args))
            finally:
                logger.info("pass")
    new_sql_conn.close()
    time.sleep(2)


@given(data_table("存在脱敏任务代理端连接B，并执行以下sql访问--循环执行42次",fixture='sql_list'))
def step_impl(page, port, sql_list):
    host = page.url.split('/')[2]
    new_sql_conn = MySql(sql_type='mysql', host=host, port=int(port), user='root', passwd='123456',
                         dbname='autotest1')
    for i in range(42):
        for sql in sql_list:
            real_sql = sql["sql_command"]
            try:
                new_sql_conn.execute_sql(real_sql)
                time.sleep(0.2)
            except ConnectionError as e:
                logger.info("连接执行失败：{}".format(e.args))
            finally:
                logger.info("pass")
    new_sql_conn.close()
    time.sleep(2)


@then(parsers.cfparse("右侧SQL操作大于[{number}]条"))
def step_impl(page, number):
    time.sleep(2)
    content = page.locator(locations_user["sql操作条数"]).text_content().strip(' ')
    a = content.split('：')[-1][:-1]
    if a == '':
        num1 = 0
    else:
        num1 = int(content.split('：')[-1][:-1])
    assert int(num1) > int(number)


@then("会话下方sql语句只展示20条")
def step_impl(page):
    time.sleep(2)
    num2 = page.locator(locations_user["右侧-sql条数"]).count()
    assert num2 == 20


# 用例95-【风险分析】验证访问用户IP页从其他界面切入且SQL操作大于40条，点击查看更多按钮展示是否正常
@when("点击sql列表下方按钮查看更多时")
def step_impl(page):
    loc = "//span[text()='点击加载更多']"
    page.locator(loc).click()
    time.sleep(1.2)


@then("会话下方sql语句多展示20条，即共展示40条数据")
def step_impl(page):
    num2 = page.locator(locations_user["右侧-sql条数"]).count()
    assert num2 == 40



import random

import allure
import pytest
from common.data_table import data_table
from playwright.sync_api import expect
from pytest_bdd import scenario, scenarios, given, when, then, parsers
from loguru import logger
import time
import datetime
from common.get_sql_config import get_sql_config
from pages.common.connection_page import ConnectionPage
from common.get_location import get_locations
from pages.common.secret_find_page import FindResult
from pages.common.secret_plan_page import SecretPlan, SecretType


locations_search = get_locations(page_name='隐私方案-方案配置', module_name='查询')
locations_list = get_locations(page_name='隐私方案-方案配置', module_name='列表')
locations_new = get_locations(page_name='隐私方案-方案配置', module_name='新建')
locations_detail = get_locations(page_name='隐私方案-方案配置', module_name='详情页')

scenarios('./common/自动化用例-隐私方案-方案配置.feature')
logger.add('../logs/mylogs/{}.txt'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))

today = str(datetime.date.today()).replace('-', '')


def get_time():
    time_stamp = str(time.time()*1000).split('.')[0]
    return time_stamp

def make_screenshot(page, case_order):
    time_stamp = str(time.time() * 1000).split('.')[0]
    allure.attach(page.screenshot(path='./test_data/screen_shots/用例{}_{}.png'.format(str(case_order), time_stamp)),
                  '页面截图_用例{}_{}'.format(str(case_order), time_stamp), allure.attachment_type.PNG)



@given("使用admin用户登录系统")
def step_impl():
    pass


@given("已经进入到'隐私方案-方案配置'页面")
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(1.5)


# 用例1-查看发现方案-页面显示内容
@given("已经在发现方案-方案配置页面")
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(1.5)


@then('应该包含:"发现方案名称","识别优先级","内置/自定义","关联数据源","描述","审批状态","更新时间","操作","查看详情","修改","删除","提交/审批"')
def step_impl(page):
    time.sleep(1)
    base_loc = "//div[@class='el-table__header-wrapper']//thead//tr//th"
    all_text = page.locator(base_loc).all_text_contents()
    name_list = ['隐私方案名称', '识别优先级', '内置/自定义', '关联数据源', '描述', '审批状态', '更新时间', '操作']
    for name in name_list:
        assert name in all_text
    other = ['首行-审批', '首行-修改', '首行-删除', '首行-查看']
    for i in other:
        loc_other = locations_list[i]
        expect(page.locator(loc_other)).to_be_visible()
    make_screenshot(page, case_order=1)


# 用例2-查看发现方案-默认方案不能修改删除及审批
@when('查看列表"默认方案"操作栏')
def step_impl():
    pass


@then("操作栏[修改][删除][审批]按钮置灰，不可点击")
def step_impl(page):
    try:
        other = ['首行-审批', '首行-修改', '首行-删除']
        time.sleep(0.1)
        for i in other:
            loc_other = locations_list[i]
            expect(page.locator(loc_other)).not_to_be_focused()
    except NotImplementedError as e:
        logger.error("no such element found:{}".format(e.args))
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_002.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例3-查看隐私方案-查看详情能否点击
@given('列表存在"默认方案"')
def step_impl(page, pages):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_conn.search("默认方案")
    time.sleep(1)
    num = new_conn.get_num()
    assert num == 1


@when("点击操作栏'查看详情'")
def step_impl(page):
    page.locator(locations_list["首行-查看"]).click()
    time.sleep(1)


@then("弹框显示方案详情")
def step_impl(page):
    expect(page.locator(locations_detail["左上角标题"])).to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_003.png'.format(today)), '页面截图', allure.attachment_type.PNG)


# 用例4-查看隐私方案-查看详情弹窗显示内容

@given("已经在默认方案详情弹框页面")
def step_impl(page, pages):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_conn.search("默认方案")
    time.sleep(1)
    page.locator(locations_list["首行-查看"]).click()


@when("查看页面内容")
def step_impl(page):
    pass


@then('包含"发现方案名称","隐私类型集合(滚动条显示)","识别优先级","指定字段类型(滚动条显示，默认5行)","关联数据源(滚动条显示，默认5行)","审批状态","审批人","审批时间","创建人","创建时间"')
def step_impl(page):
    list1 = ['方案名称','隐私类型集合框','识别优先级','指定字段类型','关联数据源集合框','描述','创建人','创建时间','更新人','更新时间','所属部门']
    for i in list1:
        loc = locations_detail[i]
        expect(page.locator(loc)).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_004.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例5-新建隐私方案-新建方案能否点击
@when("点击新建方案按钮")
def step_impl(page):
    page.locator(locations_new["新建方案"]).click()


@then("弹出新建发现方案页面")
def step_impl(page):
    loc = "//div[@role='dialog']//div[@class='el-dialog__header']//span[text()='新建隐私方案']"
    expect(page.locator(loc)).to_be_visible()


# 用例6-新建隐私方案-新建发现方案页面内容
@given("已弹出新建隐私方案页面")
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(1.5)
    page.locator(locations_new["新建方案"]).click()
    time.sleep(1)


@when("查看新建隐私方案页面")
def step_impl():
    pass


@then('页面包含:标题:"新建发现方案","字段:"*发现方案名称","*隐私类型集合(默认"默认发现全部隐私类型")","*识别优先级(默认"使用默认优先级")","指定字段类型","描述"')
def step_impl(page):
    list1 = ['默认全部隐私类型', '按需发现隐私类型', '默认优先级', '自定义优先级']
    list2 = ['方案名称', '隐私类型集合', '识别优先级', '指定字段类型', '示例', '描述']
    for i in list1:
        loc = locations_new[i]
        expect(page.locator(loc)).to_be_visible()
    contents = page.locator(locations_new["页面字段-多个"]).all_text_contents()
    for tt in list2:
        assert tt in contents[list2.index(tt)]

    make_screenshot(page, case_order=6)


# 用例7-新建发现方案-新建发现方案页面，发现方案名称是否必填
@when("隐私方案的名称输入为空")
def step_impl(page):
    page.locator(locations_new["方案名称"]).fill('')


@when("鼠标与输入框失去焦点时1")
def step_impl(page):
    page.locator(locations_new["标题-固定焦点"]).click()
    time.sleep(0.5)


@then(parsers.cfparse('下方字体提示:[{message}]'))
def step_impl(page, message):
    loc_msg = "//div[@class='el-form-item__error']"
    content = page.locator(loc_msg).text_content().strip(' ')
    assert message in content
    make_screenshot(page, case_order=12)


# 用例8-新建发现方案-新建发现方案页面，发现方案名称输入长度不大于30个字符
@when(parsers.parse("隐私方案名称输入为{name}"))
def step_impl(page, name):
    page.locator(locations_new["方案名称"]).fill(name)


@then("输入成功")
def step_impl(page):
    loc_msg = "//div[@class='el-form-item__error']"
    expect(page.locator(loc_msg)).not_to_be_visible()


# 用例9-新建隐私方案-新建隐私方案页面，隐私方案名称输入长度大于30个字符
@when(parsers.cfparse("方案名称输入为[{plan_name}]"))
def step_impl(page, plan_name):
    page.locator(locations_new["方案名称"]).fill(plan_name)


# 用例12-新建隐私方案-新建隐私方案页面，隐私方案名称不能重复


@given(parsers.cfparse("方案配置列表中已有隐私方案名称为[{plan_name}]的数据"))
def step_impl(page, pages, plan_name):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_conn.search(plan_name)
    time.sleep(0.5)
    num = new_conn.get_num()
    assert num == 1


@when(parsers.cfparse("隐私方案名称输入[{plan_name}]"))
def step_impl(page, plan_name):
    page.locator(locations_new["方案名称"]).fill(plan_name)


# 用例13-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型
@when('点击"按需选择隐私类型"')
def step_impl(page):
    page.wait_for_selector(locations_new["按需发现隐私类型"])
    page.locator(locations_new["按需发现隐私类型"]).click()


@then('下方显示穿梭框，包含:"所有","已选"')
def step_impl(page):
    loc_list = [locations_new["所有"], locations_new["已选"]]
    for i in loc_list:
        expect(page.locator(i)).to_be_visible()


# 因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-尚有争论；
@then('"所有"框中内容与隐私类型列表内容一致')
def step_impl(page, pages):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_conn.get_all_secret_type_data()
    page.goto(pages["secret_type_page"])
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    list_data = new_type.get_all_name()
    # for type1 in secret_type_list:
    #     assert type1 in list_data
    for type1 in list_data:
        assert type1 in secret_type_list
    logger.info("因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-尚有争论；")


# 用例14-验证新建隐私方案-新建隐私方案页面，新增隐私类型，按需选择隐私类型所有列表与隐私类型列表同步更新
@given('已弹出新建隐私方案页面，隐私类型集合勾选了"按需选择隐私类型"')
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(1.5)
    page.locator(locations_new["新建方案"]).click()
    page.wait_for_selector(locations_new["按需发现隐私类型"])
    page.locator(locations_new["按需发现隐私类型"]).click()
    time.sleep(1)


@then(parsers.cfparse("当前页面不存在[{secret_type}]"))
def step_impl(page, pages, secret_type):
    new_type = SecretType(base_url=pages['secret_find_page'], page=page)
    new_type.search(secret_type)
    time.sleep(1)
    if new_type.get_num() == 1:
        new_type.del_secret_type(secret_type)
    time.sleep(1)


@when(parsers.cfparse("隐私类型列表新增[{secret_type}]时"))
def step_impl(page, pages, secret_type):
    new_type = SecretType(base_url=pages['secret_find_page'], page=page)
    new_type.new_secret_type(secret_type)
    time.sleep(2)


@given(parsers.cfparse("隐私类型列表新增[{secret_type}]时"))
def step_impl(page, pages, secret_type):
    new_type = SecretType(base_url=pages['secret_find_page'], page=page)
    new_type.search(secret_type)
    time.sleep(1)
    if new_type.get_num() == 0:
        new_type.new_secret_type(secret_type)
    time.sleep(2)


@when('再次新建隐私方案，隐私类型集合勾选"按需选择隐私类型"')
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(2)
    page.locator(locations_new["新建方案"]).click()
    time.sleep(0.5)
    page.wait_for_selector(locations_new["按需发现隐私类型"])
    page.locator(locations_new["按需发现隐私类型"]).click()
    time.sleep(2)


@then(parsers.cfparse('"所有"框内内容隐私类型同步增加[{secret_type}]'))
def step_impl(page, secret_type):
    loc = locations_new["文本查找隐私类型"].format(secret_type)
    page.locator(loc).scroll_into_view_if_needed()
    assert page.locator(loc).count() == 1
    expect(page.locator(loc)).to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_014.png'.format(today)))


@when("回到隐私类型页面")
def step_impl(page, pages):
    page.goto(pages["secret_type_page"])
    time.sleep(2)


@then(parsers.cfparse("查找隐私类型[{secret_type}]并删除隐私类型成功"))
def step_impl(page, pages, secret_type):
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    new_type.search(secret_type)
    if new_type.get_num() == 1:
        new_type.del_secret_type(secret_type)


# 用例15-新建隐私方案-新建隐私方案页面，删除隐私类型，按需选择隐私类型所有列表与隐私类型列表同步更新
@given(parsers.cfparse("当前页面存在[{secret_type}]"))
def step_impl(page, secret_type):
    loc = locations_new["文本查找隐私类型"].format(secret_type)
    expect(page.locator(loc)).to_be_visible()


@when(parsers.cfparse("隐私类型列表删除[{secret_type}]时"))
def step_impl(page, pages, secret_type):
    new_type = SecretType(base_url=pages['secret_find_page'], page=page)
    new_type.del_secret_type(secret_type)


@then(parsers.cfparse('"所有"框内内容隐私类型同步去掉[{secret_type}]'))
def step_impl(page, secret_type):
    loc = locations_new["文本查找隐私类型"].format(secret_type)
    expect(page.locator(loc)).not_to_be_visible()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_015.png'.format(today)))


# 用例16-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框列表模糊筛选
@when(parsers.cfparse("所有搜索框输入[{content}]"))
def step_impl(page, content):
    page.locator(locations_new["所有搜索"]).fill(content)


@then(parsers.cfparse("下方列表框筛选出名字带[{content}]的所有隐私类型，包含有[{type1}],[{type2}]"))
def step_impl(page, content, type1, type2):
    time.sleep(0.2)
    loc1 = locations_new["文本查找隐私类型"].format(type1)
    loc2 = locations_new["文本查找隐私类型"].format(type2)
    expect(page.locator(loc1)).to_be_visible()
    expect(page.locator(loc2)).to_be_visible()
    count = page.locator(locations_new["所有隐私类型数量"]).count()
    assert count == 2
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_016.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例17-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框列表精准筛选
@then(parsers.cfparse("下方列表框筛选出名字为[{type1}]的隐私类型"))
def step_impl(page, type1):
    time.sleep(0.2)
    loc1 = locations_new["文本查找隐私类型"].format(type1)
    expect(page.locator(loc1)).to_be_visible()
    count = page.locator(locations_new["所有隐私类型数量"]).count()
    assert count == 1
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_017.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例18-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框列表筛选无匹配数据

@then('下方列表框显示"无匹配数据"')
def step_impl(page):
    page.wait_for_selector(locations_new["搜索无数据"])
    expect(page.locator(locations_new["搜索无数据"])).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_018.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例19-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框列表筛选数据清空
@when("点击所有'清空'")
def step_impl(page):
    page.locator(locations_new["所有清空"]).highlight()
    page.locator(locations_new["所有清空"]).click()
    time.sleep(0.5)


@then('"所有"框列表展示全部隐私类型与隐私类型列表中的所有隐私类型数据一致')
def step_impl(page, pages):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_conn.get_all_secret_type_data()
    page.goto(pages["secret_type_page"])
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    list_data = new_type.get_all_name()
    # for type1 in secret_type_list:
    #     assert type1 in list_data
    for type1 in list_data:
        assert type1 in secret_type_list
    logger.info("因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-尚有争论；")


# 用例20-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框单项右移功能
@when(parsers.cfparse("勾选[{type1}]"))
def step_impl(page, type1):
    page.locator(locations_new["勾选增加"].format(type1)).click()


@when("点击'>'")
def step_impl(page):
    page.locator(locations_new["向右"]).click()
    # time.sleep(1)


@then('"中文姓名信息"由"所有"框列表移至"已选"框列表')
def step_impl(page):
    pass


@then(parsers.cfparse('"所有"框无[{type1}]项'))
def step_impl(page, type1):
    loc1 = locations_new["比较查找隐私类型左"].format(type1)
    expect(page.locator(loc1)).not_to_be_visible()


@then(parsers.cfparse('"已选"框有[{type2}]项'))
def step_impl(page, type2):
    loc2 = locations_new["比较查找隐私类型右"].format(type2)
    expect(page.locator(loc2)).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_020.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例21-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框多项右移功能
@then('"中文地址信息"由"所有"框列表移至"已选"框列表')
def step_impl():
    pass


# 用例22-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框全选右移功能
@when("勾选'所有'选项")
def step_impl(page):
    page.locator(locations_new["所有"]).click()


@then("'所有'框列表所有选项全部选中")
def step_impl(page):
    loc_base = locations_new["按行序勾选"]
    count = page.locator(locations_new["所有隐私类型数量"]).count()
    for i in range(1,count+1):
        loc = loc_base.format(i)
        check = page.locator(loc).is_checked()
        assert check


@then('全部选项由"所有"框列表移至"已选"框列表')
def step_impl(page):
    pass


@then('"所有"框内容为空，"已选"框隐私类型列表中的所有隐私类型数据一致')
def step_impl(page, pages):
    page.wait_for_selector(locations_new["移动后无数据"])
    expect(page.locator(locations_new["移动后无数据"])).to_be_visible()
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_conn.get_all_secret_type_data()
    page.goto(pages["secret_type_page"])
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    list_data = new_type.get_all_name()
    # for type1 in secret_type_list:
    #     assert type1 in list_data
    for type1 in list_data:
        assert type1 in secret_type_list
    logger.info("因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-尚有争论；")


# 用例23-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框筛选右移功能
@then(parsers.cfparse('下方列表框筛选出名字带[{content}]的所有隐私类型'),target_fixture="secret_type_list")
def step_impl(page, pages, content):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_plan.get_all_secret_type_data()
    for i in secret_type_list:
        assert content in i
    return secret_type_list


@when("勾选筛选出的数据")
def step_impl(page, secret_type_list):
    for name in secret_type_list:
        page.locator(locations_new["勾选增加"].format(name)).click()


@then('勾选的选项由"所有"框列表移至"已选"框列表')
def step_impl():
    pass


@then(parsers.cfparse('"所有"框显示"无匹配数据"，"已选"框隐私类型为[{type1}]，[{type2}]'))
def step_impl(page, pages, type1, type2):
    page.wait_for_selector(locations_new["搜索无数据"])
    expect(page.locator(locations_new["搜索无数据"])).to_be_visible()
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    data = new_plan.get_all_secret_type_data(type1='right')
    assert type1 in data
    assert type2 in data
    assert len(data) == 2
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_023.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例24-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，已选框列表模糊筛选

@given('所有选项移至"已选"框列表')
def step_impl(page):
    page.locator(locations_new["所有"]).click()
    page.locator(locations_new["向右"]).click()


@when(parsers.cfparse('"已选"搜索框输入[{content}]'))
def step_impl(page, content):
    page.locator(locations_new["已选搜索"]).fill(content)


@then(parsers.cfparse('下方列表框筛选出名字带[{name}]的所有隐私类型，包含隐私类型为[{type1}]，[{type2}]'))
def step_impl(page, pages, name, type1, type2):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    data = new_plan.get_all_secret_type_data(type1='right')
    assert type1 in data
    assert type2 in data
    assert len(data) == 2
    assert name in type1 and name in type2
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_024.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例25-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，已选框列表精准筛选
@then(parsers.cfparse("下方列表框筛选出名字为[{content}]的数据"))
def step_impl(page, pages, content):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    data = new_plan.get_all_secret_type_data(type1='right')
    assert data[0] == content


# 用例27-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所选框列表筛选数据清空
@when("点击已选'清空'")
def step_impl(page):
    page.locator(locations_new["已选清空"]).highlight()
    page.locator(locations_new["已选清空"]).click()


@then('"已选"框列表展示全部数据，与隐私类型列表中的所有隐私类型数据一致')
def step_impl(page, pages):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_conn.get_all_secret_type_data()
    page.goto(pages["secret_type_page"])
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    list_data = new_type.get_all_name()
    # for type1 in secret_type_list:
    #     assert type1 in list_data
    # assert len(secret_type_list) == len(list_data)
    for type1 in list_data:
        assert type1 in secret_type_list
    logger.info("因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-此处尚有争论，先按目前逻辑实现；")


# 用例28-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框单项左移功能

@when(parsers.cfparse('"已选"框勾选[{type1}]'))
def step_impl(page, type1):
    page.locator(locations_new["勾选减少"].format(type1)).click()


@when("点击'<'")
def step_impl(page):
    page.locator(locations_new["向左"]).click()


@then('"中文姓名信息"由"已选"框列表移至"所有"框列表')
def step_impl(page):
    pass


@then(parsers.cfparse('"已选"框无[{type1}]项'))
def step_impl(page, type1):
    loc2 = locations_new["比较查找隐私类型右"].format(type1)
    expect(page.locator(loc2)).not_to_be_visible()


@then(parsers.cfparse('"所有"框有[{type2}]项'))
def step_impl(page, type2):
    loc1 = locations_new["比较查找隐私类型左"].format(type2)
    expect(page.locator(loc1)).to_be_visible()


# 用例29-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框多项左移功能
@then('"中文姓名信息"、"中文地址信息"由"已选"框列表移至"所有"框列表')
def step_impl():
    pass


# 用例30-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，穿梭框全选左移功能
@when("右侧勾选[已选]")
def step_impl(page):
    page.locator(locations_new["已选"]).click()


@then('"已选"框列表所有选项全部选中')
def step_impl(page):
    loc_base = locations_new["按行序勾选"]
    loc = locations_new["右侧内容前缀"] + locations_new["所有隐私类型数量"]
    count = page.locator(loc).count()
    for i in range(1, count + 1):
        loc = loc_base.format(i)
        check = page.locator(loc).is_checked()
        assert check


@then('全部选项由"已选"框列表移至"所有"框列表')
def step_impl():
    pass


@then('"已选"框下内容为空，"所有"框下有所有的隐私类型与隐私类型列表中的所有隐私类型数据一致')
def step_impl(page, pages):
    page.wait_for_selector(locations_new["移动后无数据-右侧"])
    expect(page.locator(locations_new["移动后无数据-右侧"])).to_be_visible()
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    secret_type_list = new_conn.get_all_secret_type_data(type1='left')
    page.goto(pages["secret_type_page"])
    new_type = SecretType(base_url=pages['secret_type_page'], page=page)
    list_data = new_type.get_all_name()
    # for type_name in secret_type_list:
    #     assert type_name in list_data
    for type1 in list_data:
        assert type1 in secret_type_list
    logger.info("因为隐私类型同步的问题，所有框中的隐私类型目前是多于隐私类型列表的内容的-尚有争论；")


# 用例31-新建隐私方案-新建隐私方案页面，隐私类型集合勾选按需选择隐私类型，所有框筛选左移功能
@then('勾选的选项由"已选"框列表移至"所有"框列表')
def step_impl():
    pass


# 用例32-新建隐私方案-新建隐私方案页面，识别优先级选择自定义优先级
@when("识别优先级勾选[自定义优先级]")
def step_impl(page):
    page.locator(locations_new["自定义优先级"]).click()


@then("下方弹出拖动框，包含:标题:拖动顺序改变优先级，顺序:自定义字典、自定义日期、自定义正则、系统内置")
def step_impl(page):
    loc1 = "//p[text()='拖动顺序改变优先级']"
    loc2 = locations_new["自定义优先级-按位置"]
    expect(page.locator(loc1)).to_be_visible()
    list_name = ['自定义字典', '自定义日期', '自定义正则', '系统内置类型']
    for i in range(1,5):
        content = page.locator(loc2.format(i)).text_content().strip(' ')
        assert content == list_name[i-1]
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_033.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例33-新建隐私方案-新建隐私方案页面，识别优先级选择自定义优先级，是否能上下拖动
@when(parsers.cfparse("拖动[{name}]向上移动一格"))
def step_impl(page, name):
    loc1 = (locations_new["自定义优先级-按名称"]).format(name)
    position1 = page.locator(loc1).bounding_box()
    position2 = page.locator(locations_new["自定义优先级-按位置"].format('3')).bounding_box()
    start_x = position1['x'] + position1['width'] / 2
    start_y = position1['y'] + position1['height'] / 2
    end_x = position2['x'] + position2['width'] / 2
    end_y = position2['y'] + (position2['height'] / 5) * 4
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    time.sleep(0.5)
    page.mouse.move(end_x, end_y)
    page.mouse.up()


@then(parsers.cfparse("当前顺序为:[{data_list}]"))
def step_impl(page, data_list):
    expect_list = data_list.split(',')
    real_list = [page.locator(locations_new["自定义优先级-按位置"].format(i)).text_content().strip(' ') for i in range(1, 5)]
    for i in range(4):
        assert expect_list[i] == real_list[i]


@when(parsers.cfparse("拖动[{name}]向下移动一格"))
def step_impl(page, name):
    time.sleep(0.1)
    loc1 = locations_new["自定义优先级-按名称"].format(name)
    position1 = page.locator(loc1).bounding_box()
    position2 = page.locator(locations_new["自定义优先级-按位置"].format('4')).bounding_box()
    start_x = position1['x'] + position1['width'] / 2
    start_y = position1['y'] + position1['height'] / 2
    end_x = position2['x'] + position2['width'] / 2
    end_y = position2['y'] + (position2['height'] / 5) * 1
    page.mouse.move(start_x, start_y)
    page.mouse.down()
    time.sleep(0.5)
    page.mouse.move(end_x, end_y)
    page.mouse.up()


# 用例34-新建隐私方案-新建隐私方案页面，指定字段类型增加一个条目
@when("指定字段类型点击'+'")
def step_impl(page):
    page.locator(locations_new["加号"]).click()
    time.sleep(0.5)


@then("第一条条目下方新增一个条目:'数据库','方案名','表名','字段名','请选择','-'")
def step_impl(page):
    # 需求更新-DT为模式名？？？
    loc_name = ['指定字段类型-数据库名', '指定字段类型-模式名', '指定字段类型-表名', '指定字段类型-字段名', '指定字段类型-请选择']
    # loc_name = ['指定字段类型-数据库名', '指定字段类型-方案名', '指定字段类型-表名', '指定字段类型-字段名', '指定字段类型-请选择']

    for i in loc_name:
        # 需求更新-DT从1 开始；之前需求从2开始
        loc = locations_new[i].format('1')
        # loc = locations_new[i].format('2')
        expect(page.locator(loc)).to_be_visible()


# 用例35-新建隐私方案-新建隐私方案页面，指定字段类型减少一个条目
@when("指定字段类型选择第一条条目点击'-'")
def step_impl(page):
    if page.locator(locations_new["减号"]).is_visible():
        page.locator(locations_new["减号"]).click()
    if page.locator(locations_new["删除按钮"]).is_visible():
        page.locator(locations_new["删除按钮"]).click()

@then("第一条条目消失")
def step_impl(page):
    loc = locations_new["指定字段类型-数据库名"].format('1')
    expect(page.locator(loc)).not_to_be_visible()


# 用例36-新建隐私方案-新建隐私方案页面，指定字段类型重复设置字段名
@given(parsers.cfparse("已新增指定字段类型column为[{name}]，隐私类型为[{type_name}]的数据"))
def step_impl(page, name, type_name):
    page.locator(locations_new["加号"]).click()
    time.sleep(0.5)
    page.locator(locations_new["指定字段类型-字段名"].format('1')).fill(name)
    # page.locator(locations_new["指定字段类型-请选择"].format('1')).click()
    if page.locator(locations_new["指定字段类型-请选择"].format('1')).focus():
        page.locator(locations_new["指定字段类型-请选择"].format('1')).click()
        time.sleep(0.5)
    else:
        page.locator(locations_new["指定字段类型-请选择"].format('2')).click()
        time.sleep(0.5)
    page.locator(locations_new["指定字段类型-下拉选择"].format(type_name)).click()


@when(parsers.cfparse("再次输入指定字段类型column为[{name}]，隐私类型为[{type_name}],点击保存"))
def step_impl(page, name, type_name):
    page.locator(locations_new["指定字段类型-字段名"].format('2')).fill(name)

    # page.locator(locations_new["指定字段类型-请选择"].format('2')).click()

    # 需求更新-DT从2 开始；之前需求从1开始
    page.locator(locations_new["指定字段类型-请选择"].format('3')).click()
    time.sleep(0.5)

    page.locator(locations_new["指定字段类型-下拉选择"].format(type_name)).click()
    page.locator(locations_new["保存"]).click()
    time.sleep(0.5)


@then(parsers.cfparse("弹框弹出错误提示[{msg}]"))
def step_impl(page, msg):
    loc1 = "//div[@role='alert']//p[text()='{}']".format(msg)
    loc2 = "//p[text()='存在同名字段，定义冲突']"
    if page.locator(loc1).is_visible():
        pass
    else:
        if page.locator(loc2).count() >= 1:
            pass
        else:
            raise


@then(parsers.cfparse("弹框弹出对应提示[{msg}]"))
def step_impl(page, msg):
    loc1 = "//div[@role='alert']//p[text()='{}']".format(msg)
    expect(page.locator(loc1)).to_be_visible()
    time.sleep(1)


# 用例37-新建隐私方案-新建隐私方案页面，描述字段输入超过200个字符
@when(parsers.cfparse("描述输入[{content}]"),target_fixture="content")
def step_impl(page, content):
    page.locator(locations_new["描述输入内容"]).fill(content)
    return content


@then("输入框内容无法继续输入")
def step_impl(page, content):
    str1 = 'afasdfasdfjasdfasldfjalskd'
    page.locator(locations_new["描述输入内容"]).fill(content+str1)
    time.sleep(1)
    text = page.locator(locations_new["字数提示"]).text_content().strip(' ')
    assert text == '200/200'


@then("输入框右下方显示为'200/200'")
def step_impl(page):
    text = page.locator(locations_new["字数提示"]).text_content().strip(' ')
    assert text == '200/200'
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_048.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例37-新建隐私方案-新建隐私方案页面，描述字段输入不超过200个字符
@when(parsers.parse("描述输入{remark}"))
def step_impl(page, remark):
    page.locator(locations_new["描述输入内容"]).fill(remark)


# 用例39-新建隐私方案-新建隐私方案页面，新建隐私方案能否成功
@given(parsers.cfparse("不存在隐私方案[{plan_name}]"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    if num == 1:
        new_plan.del_plan(plan_name)


@when(data_table("依次输入name、privacyList、identifyPriority",fixture="data_list"))
def step_impl(page, data_list):
    plan_name = data_list[0]["name"]
    page.locator(locations_new["方案名称"]).fill(plan_name)


@when("点击新建隐私方案'保存'")
def step_impl(page):
    page.locator(locations_new["保存"]).click()
    time.sleep(2.5)


@then('弹框提示:"新建成功，请提交方案并联系审批人审批"')
def step_impl(page):
    loc1 = locations_new["新建成功-标题"]
    loc2 = locations_new["新建成功-内容"]
    expect(page.locator(loc1)).to_be_visible()
    expect(page.locator(loc2)).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_039.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


@then(parsers.cfparse('返回至列表，新增一条隐私方案名称为[{plan_name}]的数据，审批状态为"未提交"，操作栏提交/审批为"提交"'))
def step_impl(page, pages, plan_name):
    page.locator(locations_new["新建成功-关闭按钮"]).click()
    time.sleep(1)
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    data = new_plan.get_line_data()
    assert data["审批状态"] == '未提交'
    content = page.locator(locations_list["首行-操作-第一个按钮"]).text_content().strip(' ')
    assert content == "提交"


# 用例40-新建隐私方案-新建隐私方案页面，取消新建隐私方案能否成功
@when("点击'取消'")
def step_impl(page):
    page.locator(locations_new["取消"]).click()


@then("页面关闭")
def step_impl(page):
    pass


@then(parsers.cfparse('返回至列表，列表无新增数据[{plan_name}]'))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    assert num == 0


# 用例41-新建隐私方案-新建隐私方案，提交隐私方案


@given(parsers.cfparse("已存在隐私方案[{plan_name}]"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    assert num == 1


@when("点击'提交'")
def step_impl(page):
    page.locator(locations_list["首行-提交"]).click()
    time.sleep(0.1)


@then(parsers.cfparse('列表[{plan_name}]审批状态变为[{status}]，操作栏展示[{button}]按钮'))
def step_impl(page, pages, plan_name, status, button):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    data = new_plan.get_line_data()
    assert data["审批状态"] == status
    content = page.locator(locations_list["首行-操作-第一个按钮"]).text_content().strip(' ')
    assert content == button


# 用例42-修改隐私方案-修改隐私方案，修改是否可点击
@when("点击'修改'")
def step_impl(page):
    page.locator(locations_list["首行-修改"]).click()


@then("弹出修改隐私方案弹窗")
def step_impl(page):
    loc_title = "//div[@class='basice-title']//span[text()='修改隐私方案']"
    expect(page.locator(loc_title)).to_be_visible()


# 用例43-修改隐私方案-修改隐私方案，修改隐私方案页面与新增是否一致
@given("已弹出修改隐私方案页面")
def step_impl(page):
    page.locator(locations_list["首行-修改"]).click()


@when("查看修改隐私方案页面")
def step_impl(page):
    pass


@then(data_table("隐私方案页面内容与新增时保持一致，数据如下表",fixture="data_list"))
def step_impl(page, data_list):
    loc = locations_new["方案名称"]
    content = page.locator(loc).input_value()
    assert content == data_list[0]["name"]
    loc1 = locations_new["默认全部隐私类型"]
    loc2 = locations_new["默认优先级"]
    for i in [loc1, loc2]:
        check1 = page.locator(i).is_checked()
        assert check1


# 用例44-修改隐私方案-修改隐私方案，修改未提交的隐私方案
@given(data_table("方案配置列表已有新增的自定义方案",fixture="new_data"))
def step_impl(page, pages, new_data):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.new_plan(new_data[0]["name"])
    time.sleep(0.2)
    new_plan.search(new_data[0]["name"])

@when('修改隐私类型集合为"按需选择发现类型-中文地址信息"，识别优先级为"自定义优先级-默认"，描述为"123"')
def step_impl(page):
    page.locator(locations_new["按需发现隐私类型"]).click()
    page.locator(locations_new["已选"]).click()
    page.locator(locations_new["向左"]).click()
    page.locator(locations_new["勾选增加"].format("中文地址信息")).click()
    page.locator(locations_new["向右"]).click()
    page.locator(locations_new["自定义优先级"]).click()
    page.locator(locations_new["描述输入内容"]).fill('123')


@then('弹出提示:修改发现方案成功！')
def step_impl(page):
    loc = locations_new["修改内容-修改成功"]
    page.wait_for_selector(loc)
    expect(page.locator(loc)).to_be_visible()
    time.sleep(0.5)
    page.locator(locations_new["新建成功-关闭按钮"]).click()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_045.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


@then(data_table("列表内容更新，数据如下表",fixture="compare_data"))
def step_impl(page, pages, compare_data):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(compare_data[0]["name"])
    data = new_plan.get_line_data()
    assert data["识别优先级"] == compare_data[0]["identifyPriority"]
    assert data["自定义"] == compare_data[0]["isBuiltIn"]
    assert data["关联数据源"] == compare_data[0]["relationConnectCount"]
    assert data["描述"] == compare_data[0]["remark"]
    assert data["审批状态"] == compare_data[0]["status"]


# 用例45-修改隐私方案-修改待审批的隐私方案
@given(parsers.cfparse("存在刚刚新建的隐私方案[{plan_name}],使用默认设置"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    if num == 1:
        new_plan.del_plan(plan_name)
    new_plan.new_plan(plan_name)
    new_plan.search(plan_name)


@when('点击"提交"')
def step_impl(page):
    page.locator(locations_list["首行-提交"]).click()


@when("点击修改")
def step_impl(page):
    page.locator(locations_list["首行-修改"]).click()


# 46.用例46-修改隐私方案-已审批的隐私方案，修改隐私类型集合、识别优先级或指定字段类型
@when(data_table("修改隐私类型集合为privacyList，识别优先级为identifyPriority，指定字段类型为assignField，描述为remark", fixture="plan_data"))
def step_impl(page, plan_data):
    secret_type1 = plan_data[0]["privacyList"].split(':')[-1]
    column = plan_data[0]["assignField"].split('-')[0]
    secret_type2 = plan_data[0]["assignField"].split('-')[-1]
    remark = plan_data[0]["remark"]
    page.locator(locations_new["按需发现隐私类型"]).click()
    time.sleep(0.1)
    page.locator(locations_new["已选"]).click()
    page.locator(locations_new["向左"]).click()
    page.locator(locations_new["勾选增加"].format(secret_type1)).click()
    page.locator(locations_new["向右"]).click()
    page.locator(locations_new["自定义优先级"]).click()
    page.locator(locations_new["加号"]).click()
    time.sleep(0.1)
    page.locator(locations_new["指定字段类型-字段名"].format('1')).fill(column)
    # page.locator(locations_new["指定字段类型-请选择"].format('1')).click()
    page.locator(locations_new["指定字段类型-请选择"].format('2')).click()
    page.locator(locations_new["指定字段类型-下拉选择"].format(secret_type2)).click()
    page.locator(locations_new["描述输入内容"]).fill(remark)


@then(parsers.cfparse("列表内容更新，优先级为[{priority}]、描述为[{remark}]、审批状态为[{status}]"))
def step_impl(page, pages, priority, remark, status):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    data = new_plan.get_line_data()
    assert data["识别优先级"] == priority
    assert data["描述"] == remark
    assert data["审批状态"] == status


# 用例47-修改隐私方案-审批退回的隐私方案，修改隐私类型集合、识别优先级或指定字段类型
@given("方案已审批退回")
def step_impl(page):
    page.locator(locations_list["首行-提交"]).click()
    page.locator(locations_list["首行-审批"]).click()
    page.locator(locations_list["审批意见"]).fill("just test")
    page.locator(locations_list["审批拒绝"]).click()


# 用例48-修改隐私方案-修改隐私方案页面，描述字段修改后超过200个字符
@given(parsers.cfparse("已经存在隐私方案[{plan_name1}]"), target_fixture="plan_name")
def step_impl(page, pages, plan_name1):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    # page.goto(pages["secret_find_page"])
    plan_name = plan_name1 + today
    new_plan.search(plan_name)
    num = new_plan.get_num()
    if num == 1:
        new_plan.del_plan(plan_name)
    new_plan.new_plan(plan_name)
    return plan_name


@given(parsers.cfparse("存在隐私方案[{plan_name}]"), target_fixture="plan_name")
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    # page.goto(pages["secret_find_page"])
    new_plan.search(plan_name)
    num = new_plan.get_num()
    if num == 1:
        new_plan.del_plan(plan_name)
    new_plan.new_plan(plan_name)
    return plan_name



# 用例49-修改隐私方案-修改隐私方案，取消修改隐私方案能否成功


@when('修改隐私类型集合为"按需选择隐私类型-中文姓名信息"，识别优先级为"自定义优先级-默认"，描述为"test1"')
def step_impl(page):
    page.locator(locations_new["按需发现隐私类型"]).click()
    page.locator(locations_new["已选"]).click()
    page.locator(locations_new["向左"]).click()
    page.locator(locations_new["勾选增加"].format("中文地址信息")).click()
    page.locator(locations_new["向右"]).click()
    page.locator(locations_new["自定义优先级"]).click()
    page.locator(locations_new["描述输入内容"]).fill('123')


@then("再次打开修改页,列表该条数据内容不变,默认发现全部隐私类型,使用默认优先级")
def step_impl(page):
    page.locator(locations_list["首行-修改"]).click()
    loc1 = locations_new["默认全部隐私类型"]
    loc2 = locations_new["默认优先级"]
    for i in [loc1, loc2]:
        check1 = page.locator(i).is_checked()
        assert check1


# 用例50-删除隐私方案-删除隐私方案，删除按钮能否点击
@when("点击'删除'按钮")
def step_impl(page):
    page.locator(locations_list["首行-删除"]).click()


@then("弹出删除提示框")
def step_impl(page):
    loc_msg = "//div[@class='delete-title' and text()='确定要删除此隐私方案吗？ ']"
    page.wait_for_selector(loc_msg)
    expect(page.locator(loc_msg)).to_be_visible()


# 用例51-删除隐私方案-删除隐私方案，删除提示页面信息
@when("查看删除提示框内容")
def step_impl():
    pass


@then("包含:标题:确认要删除此隐私方案吗？隐私方案名称:'测试方案33-temp' 提示:删除后不可找回，确定是否删除此隐私方案?按钮:'取消','确定','x'")
def step_impl(page):
    loc_list = ["删除提醒标题", "删除-隐私方案名字段", "删除提示", "删除提示内容", '删除取消', '删除确定', '删除叉号']
    for i in loc_list:
        loc = locations_list[i]
        expect(page.locator(loc)).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_051.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例52-删除隐私方案-删除隐私方案，关联数据源的隐私方案不能删除
@given("方案已审批通过")
def step_impl(page, pages, plan_name):
    new_conn = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_conn.search(plan_name)
    new_conn.approve_plan()


@given("relationConnectCount为1")
def step_impl(page, pages, plan_name):
    conn_name = "test_temp_" + today
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    mysql_conf = get_sql_config(module1="mysql",name='src-mysql57-utf8')
    values = [conn_name, mysql_conf[0], mysql_conf[1], mysql_conf[2], mysql_conf[3]]
    new_conn.new_connection(sql_type='Mysql',data_type='list',data_values=values,secret_plan=plan_name)
    time.sleep(1)
    new_conn.wait_for_find_finished(conn_name)
    time.sleep(1)
    page.goto(pages["secret_find_page"])
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)


@when("点击该条数据操作栏'删除'")
def step_impl(page):
    page.wait_for_selector(locations_list["首行-删除"])


@then("'删除'置灰不能点击")
def step_impl(page, pages):
    expect(page.locator(locations_list["首行-删除"])).not_to_be_focused()
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = "test_temp_" + today
    new_conn.search_connection(conn_name)
    new_conn.del_connection(conn_name)
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_052.png'.format(now_time)), '页面截图{}'.format(now_time), allure.attachment_type.PNG)


@when("回到数据连接页面")
def step_impl(page, pages):
    pass


@then("删除对应数据连接成功")
def step_impl(page, pages):
    new_conn = ConnectionPage(base_url=pages['connection_page'], page=page)
    conn_name = "test_temp_" + today
    new_conn.search_connection(conn_name)
    if new_conn.get_num() == 1:
        new_conn.del_connection(conn_name)
    time.sleep(1)


# 用例53-删除隐私方案-删除隐私方案，删除能否成功
@when("点击'确定'")
def step_impl(page):
    page.locator(locations_list["删除确定"]).click()


@then(parsers.cfparse("列表已无该条数据显示,[{plan_name}]删除成功"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    assert num == 0


# 用例54-删除隐私方案-删除隐私方案，取消删除能否成功
@when("点击删除'取消'")
def step_impl(page):
    page.locator(locations_list["删除取消"]).click()


@then(parsers.cfparse("返回列表，[{plan_name}]仍在列表显示"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num  = new_plan.get_num()
    assert num == 1


# 用例55-查询隐私方案-隐私方案名称模糊查询
@given(data_table("方案配置列表已有新增的自定义方案，数据如下表", fixture="plan_data"))
def step_impl(page, pages, plan_data):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    for i in plan_data:
        plan_name = i["name"]
        new_plan.search(plan_name)
        num = new_plan.get_num()
        if num != 0:
            new_plan.del_plan(plan_name)
        new_plan.new_plan(plan_name=plan_name, remark=i["remark"])
    try:
        new_plan.search(plan_data[1]["name"])
        time.sleep(0.5)
        new_plan.approve_plan()
        new_plan.search(plan_data[2]["name"])
        time.sleep(0.5)
        page.locator(locations_list["首行-提交"]).click()
        new_plan.search(plan_data[3]["name"])
        time.sleep(0.5)
        page.locator(locations_list["首行-提交"]).click()
        time.sleep(0.5)
        page.locator(locations_list["首行-审批"]).click()
        page.locator(locations_list["审批意见"]).fill("just test")
        page.locator(locations_list["审批拒绝"]).click()
    except NotImplementedError as e:
        logger.error("make sure if element is no found:{}".format(e.args))


@when(parsers.cfparse("在方案名称输入[{plan_name}]"))
def step_impl(page, plan_name):
    page.locator(locations_search["隐私方案名称"]).fill(plan_name)


@when("点击'查询'")
def step_impl(page):
    page.locator("button:has-text(\"查询\")").click()


@then('列表筛选出隐私方案名称带"方案1"的所有数据,包含：\'auto-测试方案1-temp\',\'auto-开发方案1\',\'auto-产品方案1\'')
def step_impl(page, pages):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    list1 = []
    for i in range(1,num+1):
        name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
        list1.append(name)
    list2 = ['auto-测试方案1-temp', 'auto-开发方案1', 'auto-产品方案1']
    for name in list2:
        assert name in list1
    assert "auto-通用方案" not in list1


# 用例56-查询隐私方案-隐私方案名称精准查询
@given("列表存在隐私方案[默认方案],[auto-测试方案1-temp],[auto-开发方案1 ],[auto-产品方案1],[auto-通用方案]")
def step_impl():
    pass
    # 上个场景已实现数据的构造


@then(parsers.cfparse("列表筛选出方案名称为[{plan_name}]的数据"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    assert num == 1
    name = page.locator(locations_list["其他行-方案名"].format('1')).text_content().strip(' ')
    assert name == plan_name


# 用例57-查询隐私方案-内置/自定义查询
@when(parsers.cfparse("内置/自定义选择[{choice}]"))
def step_impl(page, choice):
    page.locator(locations_search["内置输入框"]).click()
    page.locator(locations_search["内置下拉选择"].format(choice)).click()


@then(parsers.cfparse("列表筛选出多条数据,包含：[{plan_list}]"))
def step_impl(page, pages, plan_list):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    list1 = []
    if num <= 10:
        for i in range(1, num+1):
            name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
            list1.append(name)
    else:
        for i in range(1, 11):
            name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
            list1.append(name)
    new_list = plan_list.split(',')
    for name in new_list:
        assert name in list1
    assert "默认方案" not in list1
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_055.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例58-查询隐私方案-审批状态查询
@when(parsers.cfparse("审批状态选择[{status}]"))
def step_impl(page, status):
    page.locator(locations_search["审批状态输入框"]).click()
    page.locator(locations_search["审批状态下拉选择"].format(status)).click()


@then(parsers.cfparse("列表筛选出方案名称包括[{plan_name}]的数据"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    list1 = []
    for i in range(1,num+1):
        name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
        list1.append(name)
    assert plan_name in list1


# 用例59-2-查询隐私方案-更新时间查1询

@when("更新时间开始和结束输入为今天")
def step_impl(page):
    today1 = str(datetime.date.today())
    page.locator(locations_search["更新时间-开始日期"]).fill(today1)
    page.locator(locations_search["更新时间-结束日期"]).fill(today1)


@then("列表筛选数据,更新时间均为今天")
def step_impl(page, pages):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    list1 = []
    if num <= 10:
        for i in range(1, num+1):
            name = page.locator(locations_list["其他行-更新时间"].format(i)).text_content().strip(' ').split(' ')[0]
            list1.append(name)
    else:
        for i in range(1, 11):
            name = page.locator(locations_list["其他行-更新时间"].format(i)).text_content().strip(' ').split(' ')[0]
            list1.append(name)
    today = str(datetime.date.today())
    for j in list1:
        assert j == today


# 用例60-查询隐私方案-组合查询
@when("输入隐私方案名称，内置/自定义，审批状态选择，更新时间为今天")
def step_impl():
    pass


@then(data_table("点击'查询'，查询成功，列表筛选数据包含对应的search_result结果", fixture="search_data"))
def step_impl(page, pages, search_data):
    today1 = str(datetime.date.today())
    count = len(search_data)
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    for search in search_data:
        page.locator(locations_search["重置按钮"]).click()

        if search["name"] != "NULL":
            page.locator(locations_search["隐私方案名称"]).fill(search["name"])
        if search['isbuiltin'] != "NULL":
            page.locator(locations_search["内置输入框"]).click()
            page.locator(locations_search["内置下拉选择"].format(search['isbuiltin'])).click()
        if search['status'] != "NULL":
            page.locator(locations_search["审批状态输入框"]).click()
            page.locator(locations_search["审批状态下拉选择"].format(search['status'])).click()
        page.locator(locations_search["更新时间-开始日期"]).fill(today1)
        page.locator(locations_search["更新时间-结束日期"]).fill(today1)

        page.locator("button:has-text(\"查询\")").click()
        time.sleep(1.2)

        num = new_plan.get_num()
        if num == 0:
            assert search['search_result'] == 'NULL'
        elif num <= 10:
            list1 = []
            for i in range(1, num+1):
                name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
                list1.append(name)
            exp_list = search['search_result'].split(',')
            for plan_name in exp_list:
                assert plan_name in list1
        else:
            list1 = []
            for i in range(1, 11):
                name = page.locator(locations_list["其他行-方案名"].format(i)).text_content().strip(' ')
                list1.append(name)
            exp_list = search['search_result'].split(',')
            for plan_name in exp_list:
                assert plan_name in list1


# 用例61-查询隐私方案-查询不到数据
@then("列表返回空")
def step_impl(page, pages):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    assert num == 0


# 用例62-查询隐私方案-重置能否成功
@when("点击查询'重置'")
def step_impl(page):
    page.locator(locations_search["重置按钮"]).click()


@then("列表返回至第1页，展示所有数据")
def step_impl(page, pages):
    loc1 = "//input[@type='number']"
    value = page.locator(loc1).input_value()
    assert value == '1'
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    num = new_plan.get_num()
    assert num > 1

@then("查询框内所有查询条件内容清空")
def step_impl(page):
    loc_name1 = locations_search["隐私方案名称"]
    value = page.locator(loc_name1).input_value()
    assert value == ""


# 用例63-审批隐私方案-是否只有安全管理员能进行审批

# 用例64-审批隐私方案-方案审批弹窗显示内容
@given(parsers.cfparse("列表存在隐私方案[{plan_name}],方案状态为待审批"))
def step_impl(page, pages, plan_name ):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    assert num == 1
    status = page.locator(locations_list["首行-审批状态"]).text_content().strip(' ')
    assert status == '待审批'


@when("点击操作栏'审批'")
def step_impl(page):
    page.locator(locations_list["首行-审批"]).click()
    time.sleep(1)


@then("弹出方案审批弹窗")
def step_impl():
    pass


@then("弹窗内容包含:标题:'方案审批',隐私方案名称:'auto-产品方案1',列表字段:'修改类别','修改前','修改后','修改人','修改时间',审批意见,按钮:'审批退回','审批通过','x'")
def step_impl(page):
    loc1 = "//div[@class='el-dialog__header']/span[text()='方案审批']"
    loc_base = "//div[@class='el-dialog__body']//label[text()='{}']"
    loc_name = ['隐私方案名称：','隐私类型集合：','识别优先级：','指定字段类型：','描述：','审批意见：']
    expect(page.locator(loc1)).to_be_visible()
    for i in loc_name:
        expect(page.locator(loc_base.format(i))).to_be_visible()
    expect(page.locator(locations_list["审批通过"])).to_be_visible()
    expect(page.locator(locations_list["审批拒绝"])).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_064.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例65-审批隐私方案-审批通过能否成功
@given("已弹出方案审批弹窗")
def step_impl(page):
    page.locator(locations_list["首行-审批"]).click()


@when("点击'审批通过'")
def step_impl(page):
    page.locator(locations_list["审批通过"]).click()
    time.sleep(0.2)


@then(parsers.cfparse('列表[{plan_name}]审批状态更新为[{status}]，操作栏"审批"按钮置灰'))
def step_impl(page, pages, plan_name, status):
    status1 = page.locator(locations_list["首行-审批状态"]).text_content().strip(' ')
    assert status1 == status
    expect(page.locator(locations_list["首行-审批"])).not_to_be_focused()


# 用例66-审批隐私方案-审批退回不填写审批意见能否成功
@given("方案已提交")
def step_impl(page):
    page.locator(locations_list["首行-提交"]).click()
    time.sleep(1.2)


@when("点击'审批退回'")
def step_impl(page):
    page.locator(locations_list["审批拒绝"]).click()


# @then("审批意见框标红")
# def step_impl():
#     raise NotImplementedError(u'STEP: Then 审批意见框标红')


@then('下方字体提示:"若需退回,审批意见不能为空"')
def step_impl(page):
    loc_info = "//div[@class='el-form-item__error' and contains(text(),'若需退回，审批意见不可为空')]"
    expect(page.locator(loc_info)).to_be_visible()
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_066.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例67-审批隐私方案-审批退回填写审批意见能否成功
@when(parsers.cfparse("审批意见填写[{content}]"))
def step_impl(page, content):
    page.locator(locations_list["审批意见"]).fill(content)


@then("页面关闭，返回列表")
def step_impl(page):
    pass


@then(parsers.cfparse("列表数据[{plan_name}]审批状态更新为[{status}]，操作栏'审批'按钮变为'提交'"))
def step_impl(page, pages, plan_name, status):
    status1 = page.locator(locations_list["首行-审批状态"]).text_content().strip(' ')
    assert status1 == status
    expect(page.locator(locations_list["首行-提交"])).to_be_visible()


# 用例68-审批隐私方案-取消审批能否成功
@when("点击'x'")
def step_impl(page):
    page.locator(locations_list["审批叉号"]).click()


@then(parsers.cfparse("列表数据[{plan_name}]审批状态更新为[{status}]，操作栏按钮为'审批'"))
def step_impl(page, pages, plan_name, status):
    status1 = page.locator(locations_list["首行-审批状态"]).text_content().strip(' ')
    assert status1 == status
    expect(page.locator(locations_list["首行-审批"])).to_be_visible()


# Scenario: 用例69-审批隐私方案-方案审批弹窗，修改类别为加入方案
@when(parsers.cfparse("隐私方案[{plan_name}]审批通过"))
def step_impl(page, plan_name):
    page.locator(locations_list["首行-提交"]).click()
    time.sleep(0.5)
    page.locator(locations_list["首行-审批"]).click()
    time.sleep(0.5)
    page.locator(locations_list["审批通过"]).click()
    time.sleep(0.5)


@when(parsers.cfparse('修改[{plan_name}]添加指定字段隐私方案[{column}]:[{type1}]'))
def step_impl(page, plan_name, column, type1):
    page.locator(locations_list["首行-修改"]).click()
    page.locator(locations_new["加号"]).click()
    page.locator(locations_new["指定字段类型-字段名"].format('1')).fill(column)

    # page.locator(locations_new["指定字段类型-请选择"].format('1')).click()
    # DT为2
    page.locator(locations_new["指定字段类型-请选择"].format('2')).click()
    page.locator(locations_new["指定字段类型-下拉选择"].format(type1)).click()
    page.locator(locations_new["保存"]).click()
    page.locator(locations_new["新建成功-关闭按钮"]).click()


@when("点击'审批'")
def step_impl(page):
    page.locator(locations_list["首行-审批"]).click()
    time.sleep(1)


@then("查看'方案审批'页面")
def step_impl():
    pass


@then(parsers.cfparse('修改类别显示为[{update_type}]，修改前显示为[{content_before}],修改后显示为[{content_after}]'))
def step_impl(page, update_type, content_before, content_after):
    update = page.locator(locations_list["二次审批-修改类别"]).text_content().strip(' ')
    content1 = page.locator(locations_list["二次审批-修改前减"]).text_content().strip(' ')
    content2 = page.locator(locations_list["二次审批-修改后"]).text_content().strip(' ')
    assert update == update_type
    assert content1 == content_before
    assert content2 == content_after
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_069.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例70-审批隐私方案-方案审批弹窗，修改类别为移出方案
@given(parsers.cfparse("存在刚刚审批通过的隐私方案[{plan_name}]"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.search(plan_name)
    num = new_plan.get_num()
    assert num == 1
    page.locator(locations_list["首行-审批"]).click()
    page.locator(locations_list["审批通过"]).click()
    new_plan.search(plan_name)


@when('修改"auto-测试方案4-temp"删除指定字段隐私方案[Email]:[中文地址信息]')
def step_impl(page):
    page.locator(locations_list["首行-修改"]).click()

    if page.locator(locations_new["减号"]).is_visible():
        page.locator(locations_new["减号"]).click()
    if page.locator(locations_new["删除按钮"]).is_visible():
        page.locator(locations_new["删除按钮"]).click()

    page.locator(locations_new["保存"]).click()
    page.locator(locations_new["新建成功-关闭按钮"]).click()


@then(parsers.cfparse('最新修改类别显示为[{update_type}]，修改前显示为[{content_before}],修改后显示为[{content_after}]'))
def step_impl(page, update_type, content_before, content_after):
    lines = page.locator(locations_list["二次审批-行数"]).count()
    update = page.locator(locations_list["二次审批-其他行-修改类别"].format(lines)).text_content().strip(' ')
    content1 = page.locator(locations_list["二次审批-其他行-修改前"].format(lines)).text_content().strip(' ')
    content2 = page.locator(locations_list["二次审批-其他行-修改后减"].format(lines)).text_content().strip(' ')
    assert update == update_type
    assert content1 == content_before
    assert content2 == content_after
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_070.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# 用例71-审批隐私方案-方案审批弹窗，修改类别为修改
@when(parsers.cfparse("修改[{plan_name}]调整内置隐私类型优先级为'第一位'"))
def step_impl(page, pages, plan_name):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    new_plan.update_priority(rule_name="系统内置类型")


@then(parsers.cfparse('最新的修改类别显示为[{update_type}]，修改前显示为[{content_before}],修改后显示为[{content_after}]'))
def step_impl(page, update_type, content_before, content_after):
    lines = page.locator(locations_list["二次审批-行数"]).count()
    update = page.locator(locations_list["二次审批-其他行-修改类别"].format(lines)).text_content().strip(' ')
    content1 = page.locator(locations_list["二次审批-其他行-修改前"].format(lines)).text_content().strip(' ')
    content2 = page.locator(locations_list["二次审批-其他行-修改后"].format(lines)).text_content().strip(' ')
    assert update == update_type
    assert content1 == content_before
    assert content2 == content_after
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_071.png'.format(now_time)),
                  '页面截图{}'.format(now_time), allure.attachment_type.PNG)


# END：用例72-end-后置处理-删除隐私方案测试数据
@given("已进入隐私方案配置页面")
def step_impl(page):
    pass


@when("存在用例集新建的隐私测试方案，删除这些方案")
def step_impl(page, pages):
    new_plan = SecretPlan(base_url=pages['secret_find_page'], page=page)
    plan_list1 = ['自定义隐私类型a1', '自定义隐私类型a2', '测试方案1-temp1', '测试方案1-temp2', '测试方案a-temp1', '测试方案101-temp', '测试方案2-temp', 'auto-测试方案-update1', 'auto-测试方案-update2', '测试方案44-temp', '测试方案4-temp', '测试方案5-temp', 'auto-测试方案11-temp', 'auto-开发方案1', 'auto-产品方案1', 'auto-通用方案', 'auto-测试方案2-temp', 'auto-开发方案2', 'auto-产品方案2', 'auto-通用方案2', 'auto-测试方案11-temp', 'auto2-测试方案2-temp', 'auto2-测试方案1-temp', 'auto-测试方案3-temp', 'auto-测试方案4-temp', 'auto-测试方案5-temp']
    plan_list2 = ['测试方案44-temp', 'auto-通用方案', 'auto-测试方案b-temp', 'auto-开发方案b', 'auto-产品方案b', 'auto-通用方案b', 'auto1-产品方案1', 'auto2-产品方案2']
    all_list = plan_list1 + plan_list2
    for plan in all_list:
        new_plan.search(plan)
        num = new_plan.get_num()
        if num == 1:
            new_plan.del_plan(plan)


@then("删除成功")
def step_impl():
    pass


@then(parsers.cfparse("搜索并删除隐私方案[{secret_plan}]成功"))
def step_impl(page, pages, secret_plan, plan_name):
    new_type = SecretPlan(base_url=pages['secret_type_page'], page=page)
    new_type.search(plan_name)
    if new_type.get_num() == 1:
        new_type.del_plan(plan_name)
    now_time = get_time()
    allure.attach(page.screenshot(path='./test_data/screen_shots/{}_001.png'.format(now_time)), '页面截图{}'.format(now_time), allure.attachment_type.PNG)


@then(parsers.cfparse("搜索删除隐私方案[{secret_plan}]成功"))
def step_impl(page, pages, secret_plan):
    new_type = SecretPlan(base_url=pages['secret_type_page'], page=page)
    new_type.search(secret_plan)
    if new_type.get_num() == 1:
        new_type.del_plan(secret_plan)


@when("回到隐私方案页面")
def step_impl(page, pages):
    page.goto(pages['secret_find_page'])
    time.sleep(1)


@then(parsers.cfparse("搜索并删除隐私方案列表[{plan_list}]成功"))
def step_impl(page, pages, plan_list):
    new_type = SecretPlan(base_url=pages['secret_type_page'], page=page)
    plans = plan_list.split(',')
    for plan in plans:
        new_type.search(plan)
        if new_type.get_num() == 1:
            new_type.del_plan(plan)

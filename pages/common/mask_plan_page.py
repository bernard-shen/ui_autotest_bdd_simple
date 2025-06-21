from playwright.sync_api import Page
from base.dta.web_ui_dta_conf_reader import WebUIDtaConfReader
from pages.location_config.dta_pages import new_connect
from loguru import logger
import time
from common.get_location import get_locations


logger.add('../../logs/pages/secret_find_page_{}.txt'.format(time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())))


class MaskPlan:
    # 初始化，加载配置和xpath
    def __init__(self, base_url, page: Page):
        self.base_url = base_url
        self.page = page
        self.pages = WebUIDtaConfReader().config.pages
        self.s = lambda css: self.page.query_selector(css)
        self.locations_search = get_locations(page_name='脱敏方案-方案配置',module_name='查询')
        self.locations_list = get_locations(page_name='脱敏方案-方案配置', module_name='列表')
        self.locations_new = get_locations(page_name='脱敏方案-方案配置', module_name='新建')
        self.locations_detail = get_locations(page_name='脱敏方案-方案配置', module_name='详情页')
        self.locations_approve = get_locations(page_name='脱敏方案-方案配置', module_name='审批页')

    # 查询后获取数据条数
    def get_num(self):
        num = int(self.page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
        return num

    # 查询
    def search(self, plan_name):
        if self.page.url != self.pages["dt_mask_plan_page"]:
            self.page.goto(self.pages["dt_mask_plan_page"])
        self.page.locator(self.locations_search["脱敏方案名称"]).fill(plan_name)
        self.page.locator(self.locations_search["查询按钮"]).click()
        time.sleep(1)
        return self.page

    # 所有条件查询
    def full_search(self, plan_name=None, built_in=None, approve_status=None, update_time=None):
        if self.page.url != self.pages["dt_mask_plan_page"]:
            self.page.goto(self.pages["dt_mask_plan_page"])
        time.sleep(1)
        if plan_name:
            if plan_name not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["脱敏方案名称"]).fill(plan_name)
        if built_in:
            if built_in not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["内置自定义"]).click()
                self.page.locator(self.locations_search["内置自定义下拉选择"].format(built_in)).click()
        if approve_status:
            if approve_status not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["审批状态"]).click()
                self.page.locator(self.locations_search["审批状态下拉选择"].format(approve_status)).click()
        if update_time:
            if update_time not in ["NULL", 'null', '']:
                start_time = update_time.split('~')[0]
                end_time = update_time.split('~')[1]
                self.page.locator(self.locations_search["更新时间-开始"]).fill(start_time)
                self.page.locator(self.locations_search["更新时间-结束"]).fill(end_time)

        self.page.locator(self.locations_search["查询按钮"]).click()
        time.sleep(1)
        return self.page

    # 新建脱敏方案
    def new_plan(self, plan_name, secret_type, mask_rule):
        if self.page.url != self.pages["dt_mask_plan_page"]:
            self.page.goto(self.pages["dt_mask_plan_page"])
        time.sleep(1)
        self.page.locator(self.locations_new["新建方案"]).click()
        self.page.locator(self.locations_new["方案名称"]).fill(plan_name)
        self.page.locator(self.locations_new["隐私类型搜索"]).click()
        self.page.locator(self.locations_new["隐私类型搜索"]).fill(secret_type)
        self.page.locator(self.locations_new["脱敏规则点击"].format(secret_type)).click()
        self.page.locator(self.locations_new["脱敏规则下拉选择"].format(mask_rule)).click()
        self.page.locator(self.locations_new["保存按钮"]).click()
        self.page.locator(self.locations_new["关闭"]).click()
        return self.page

    # 快速新增方案
    def quick_new(self, plan_name):
        if self.page.url != self.pages["dt_mask_plan_page"]:
            self.page.goto(self.pages["dt_mask_plan_page"])
        self.page.locator(self.locations_new["新建方案"]).click()
        self.page.locator(self.locations_new["方案名称"]).fill(plan_name)
        self.page.locator(self.locations_new["保存按钮"]).click()
        time.sleep(1.5)
        self.page.locator(self.locations_new["关闭"]).click()
        return self.page

    # 方案审批通过
    def approve(self, plan_name):
        self.search(plan_name)
        if self.page.locator(self.locations_list["列表-首行-按钮-提交"]).is_visible():
            self.page.locator(self.locations_list["列表-首行-按钮-提交"]).click()
        if self.page.locator(self.locations_list["列表-首行-按钮-审批"]).is_visible():
            self.page.locator(self.locations_list["列表-首行-按钮-审批"]).click()
        if self.page.locator(self.locations_list["审批通过"]).is_visible():
            self.page.locator(self.locations_list["审批通过"]).click()
            time.sleep(0.5)
        return self.page

    # 方案审批退回
    def refuse_approve(self):
        self.page.locator(self.locations_list["列表-首行-按钮-提交"]).click()
        self.page.locator(self.locations_list["列表-首行-按钮-审批"]).click()
        self.page.wait_for_selector(self.locations_list["审批意见"])
        self.page.locator(self.locations_list["审批意见"]).fill('just a test.')
        self.page.locator(self.locations_list["审批退回"]).click()
        time.sleep(1)
        return self.page

    # 获取新建页，隐私类型 和 脱敏规则数据
    def get_new_data(self, search_content=None):
        if search_content:
            self.page.locator(self.locations_new["隐私类型搜索"]).fill(search_content)
        lines = self.page.locator(self.locations_new["隐私类型行数"]).count()
        list_temp = []
        for line in range(1, lines+1):
            dict_temp = {}
            secret_type1 = self.page.locator(self.locations_new["不同隐私类型名称"].format(line)).text_content().strip(' ')
            mask_rule_loc = self.locations_new["脱敏规则点击"].format(secret_type1)
            mask_rule = self.page.locator(mask_rule_loc).input_value()
            dict_temp['隐私类型'] = secret_type1
            dict_temp["脱敏规则"] = mask_rule
            list_temp.append(dict_temp)
        return list_temp

    # 获取列表数据
    def get_line_data(self):
        lines = self.page.locator(self.locations_list["列表行数"]).count()
        list_temp = []
        loc_name1 = ['列表-脱敏方案名称', '列表-内置-自定义', '列表-创建人', '列表-更新时间', '列表-审批状态']
        loc_name2 = ['列表-描述-无内容', '列表-描述-有内容']
        for line in range(1, lines+1):
            dict_temp = {}
            for loc in loc_name1:
                content1 = self.page.locator(self.locations_list[loc].format(line)).text_content().strip(' ')
                key1 = loc.split('-')[-1]
                dict_temp[key1] = content1
            remark_loc1 = self.locations_list[loc_name2[0]].format(line)
            remark_loc2 = self.locations_list[loc_name2[1]].format(line)

            if self.page.locator(remark_loc2).count() == 1:
                content2 = self.page.locator(remark_loc2).text_content().strip(' ')
                key2 = loc_name2[1].split('-')[1]
                dict_temp[key2] = content2
            elif self.page.locator(remark_loc1).count() == 1:
                content2 = self.page.locator(remark_loc1).text_content().strip(' ')
                key2 = loc_name2[0].split('-')[1]
                dict_temp[key2] = content2
            else:
                logger.error("element not found!:{}{}".format(remark_loc1, remark_loc2))
            list_temp.append(dict_temp)
        return list_temp

    # 获取二次审批页面数据
    def get_again_approve_data(self):
        lines = self.page.locator(self.locations_approve["二次审批-表内容行数"]).count()
        list_temp = []
        loc_name = ['二次审批-修改项', '二次审批-隐私类型', '二次审批-修改前', '二次审批-修改后', '二次审批-修改人', '二次审批-修改时间']
        for line in range(1, lines+1):
            dict_temp = {}
            for loc in loc_name:
                if loc in ['二次审批-修改前', '二次审批-修改后']:
                    content1 = self.page.locator(self.locations_approve[loc].format(line)).inner_text().strip(' ')
                else:
                    content1 = self.page.locator(self.locations_approve[loc].format(line)).text_content().strip(' ')
                key = loc.split('-')[-1]
                dict_temp[key] = content1
            list_temp.append(dict_temp)
        return list_temp

    # 删除脱敏方案
    def del_plan(self):
        time.sleep(1)
        # self.page.wait_for_selector(self.locations_list["操作-更多"].format('1'))
        # self.page.locator(self.locations_list["操作-更多"].format('1')).click()
        self.page.locator('.el-table__fixed-right  .more > span').click()
        time.sleep(1)
        self.page.locator(self.locations_list["操作-更多-删除"].format('1')).click()
        time.sleep(0.2)
        self.page.locator(self.locations_list["删除弹框-确定"]).click()
        return self.page


class MaskRule:
    # 初始化
    def __init__(self, base_url, page: Page):
        self.base_url = base_url
        self.page = page
        self.pages = WebUIDtaConfReader().config.pages
        self.s = lambda css: self.page.query_selector(css)
        self.locations_search = get_locations(page_name='脱敏方案-脱敏规则',module_name='查询')
        self.locations_new = get_locations(page_name='脱敏方案-脱敏规则', module_name='新建')
        self.locations_list = get_locations(page_name='脱敏方案-脱敏规则', module_name='列表')

    # 查询后获取数据条数
    def get_num(self):
        num = int(self.page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
        return num

    # 查询
    def search(self, plan_name):
        if self.page.url != self.pages["dt_mask_rule_page"]:
            self.page.goto(self.pages["dt_mask_rule_page"])
        time.sleep(1)
        self.page.locator(self.locations_search["脱敏方案名称"]).fill(plan_name)
        self.page.locator(self.locations_search["查询按钮"]).click()
        time.sleep(1.5)
        return self.page

    # 新建脱敏规则
    def new_rule(self, rule_name, secret_type, alg_choice):
        if self.page.url != self.pages["dt_mask_rule_page"]:
            self.page.goto(self.pages["dt_mask_rule_page"])
        time.sleep(1)
        self.page.locator(self.locations_new["新建脱敏规则"]).click()
        self.page.locator(self.locations_new["规则名"]).fill(rule_name)
        self.page.locator(self.locations_new["隐私类型点击"]).click()
        time.sleep(0.2)
        self.page.locator(self.locations_new["隐私类型下拉选择"].format(secret_type)).click()
        self.page.locator(self.locations_new["脱敏算法点击"]).click()
        self.page.locator(self.locations_new["脱敏算法下拉选择"].format(alg_choice)).click()
        self.page.locator(self.locations_new["保存按钮"]).click()
        self.page.locator(self.locations_new["关闭"]).click()
        return self.page

    # 删除脱敏规则
    def del_rule(self):
        self.page.locator(self.locations_list["第一行更多按钮"]).click()
        time.sleep(0.5)
        self.page.locator(self.locations_list["第一行删除按钮"]).click()
        time.sleep(0.5)
        self.page.locator(self.locations_list["确定按钮"]).click()
        time.sleep(0.5)
        return self.page


class MaskAlgorithm:
    # 初始化
    def __init__(self, base_url, page: Page):
        self.base_url = base_url
        self.page = page
        self.pages = WebUIDtaConfReader().config.pages
        self.s = lambda css: self.page.query_selector(css)
        self.locations_search = get_locations('脱敏方案-脱敏算法', '查询')
        self.locations_new = get_locations('脱敏方案-脱敏算法', '新建')
        self.locations_list = get_locations('脱敏方案-脱敏算法', '列表')
        self.locations_update = get_locations('脱敏方案-脱敏算法', '修改')

    # 获取数据条数
    def get_num(self):
        num = int(self.page.locator('//span[@class="el-pagination__total"]').text_content().split(' ')[1])
        return num

    # 查询
    def search(self, algorithm_name=None, algorithm_classification=None, algorithm_type=None, create_type=None):
        if self.page.url != self.pages["dt_mask_algorithm_page"]:
            self.page.goto(self.pages["dt_mask_algorithm_page"])
        time.sleep(0.8)
        if algorithm_name:
            if algorithm_name not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["算法名称"]).fill(algorithm_name)
        if algorithm_classification:
            if algorithm_classification not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["算法分类"]).click()
                self.page.locator(self.locations_search["下拉选择通用"].format(algorithm_classification)).click()
        if algorithm_type:
            if algorithm_type not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["类型"]).click()
                self.page.locator(self.locations_search["下拉选择通用"].format(algorithm_type)).click()
        if create_type:
            if create_type not in ["NULL", 'null', '']:
                self.page.locator(self.locations_search["创建方式"]).click()
                self.page.locator(self.locations_search["下拉选择通用"].format(create_type)).click()
        time.sleep(0.2)
        self.page.locator(self.locations_search["查询按钮"]).click()
        time.sleep(2)
        return self.page

    # 新建脱敏算法
    def new_algorithm(self, algorithm_name, code_text, remark=None, view_text=None):
        if self.page.url != self.pages["dt_mask_algorithm_page"]:
            self.page.goto(self.pages["dt_mask_algorithm_page"])
        time.sleep(1)
        self.page.locator(self.locations_new["自定义算法按钮"]).click()
        self.page.locator(self.locations_new["算法名称"]).fill(algorithm_name)
        # 取前四位
        default_code1 = "str = str.substring(0,4);"
        # 末尾加1950
        default_code2 = "str = str + 'A'*30;"
        # 开头拼加AAAAA
        default_code3 = "String str1='AAAAA';\nstr = str1.concat(str);"
        if code_text == 1:
            self.page.locator(self.locations_new["代码编译框"]).fill(default_code1)
        elif code_text == 2:
            self.page.locator(self.locations_new["代码编译框"]).fill(default_code2)
        elif code_text == 3:
            self.page.locator(self.locations_new["代码编译框"]).fill(default_code3)
        else:
            self.page.locator(self.locations_new["代码编译框"]).fill(code_text)
        if remark:
            self.page.locator(self.locations_new["描述"]).fill(remark)
        if view_text:
            self.page.locator(self.locations_new["效果预览-脱敏前"]).fill(view_text)

        self.page.locator(self.locations_new["保存"]).click()
        time.sleep(1)
        return self.page

    # 删除脱敏算法
    def del_algorithm(self, name):
        if self.page.url != self.pages["dt_mask_algorithm_page"]:
            self.page.goto(self.pages["dt_mask_algorithm_page"])
        time.sleep(1)
        self.search(algorithm_name=name)
        self.page.locator(self.locations_search["查询按钮"]).click()
        time.sleep(1)
        self.page.locator(self.locations_list["删除按钮"]).click()
        time.sleep(0.5)
        self.page.locator(self.locations_list["删除确定"]).click()
        return self.page

    # 算法还原默认参数设置
    def reset(self):
        self.page.locator(self.locations_list["修改按钮"]).click()
        time.sleep(1.5)
        self.page.locator(self.locations_update["还原默认参数"]).click()
        self.page.locator(self.locations_update["保存"]).click()
        time.sleep(0.5)
        return self.page

    # 算法查看页详情内容
    def get_detail(self):
        loc_list = ['算法名称', '分类', '类型', '创建方式', '描述', '创建人', '创建时间', '更新人', '更新时间']
        base_loc = self.locations_list["查看-通用内容"]
        content_dict = {}
        for loc in loc_list:
            text1 = self.page.locator(base_loc.format(loc)).text_content().strip(' ')
            content_dict[loc] = text1
        return content_dict

    # 获取列表首行数据
    def get_line_data_list(self):
        base_loc = self.locations_list["首行-所有"]
        all_text = self.page.locator(base_loc).all_text_contents()
        list_temp = all_text[:5]
        new_text = list_temp[1].strip(' ').split(' ')[0]
        list_temp[1] = new_text
        return list_temp

    # 获取列表当前页数据
    def get_page_line_data(self):
        base_loc = self.locations_list["其他行-所有"]
        base_list = ['算法名称', '算法分类', '类型', '创建方式', '描述']
        result_list = []
        num = self.get_num()
        if num > 10:
            num = 10
        if num != 0:
            for line in range(1, num+1):
                all_text = self.page.locator(base_loc.format(str(line))).all_text_contents()
                list_temp = all_text[:5]
                new_text = list_temp[1].strip(' ').split(' ')[0]
                list_temp[1] = new_text
                dict_temp = dict(zip(base_list,list_temp))
                result_list.append(dict_temp)
        return result_list




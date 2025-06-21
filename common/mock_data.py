#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--
import random
import time
import datetime
from faker import Faker
from faker.providers import BaseProvider
from sql_connect import MySql


fake = Faker('zh-CN')


class MyProvider(BaseProvider):
######################## 17种内置隐私类型 ##############################################

    # 1、中文地址--可变长地址--限制长度500以内
    @staticmethod
    def get_address(length=None):
        if length:
            base_str = ''
            for i in range(50):
                base_str += fake.address()
            final_address = base_str[:length]
            return final_address
        else:
            return fake.address()

    # 2、银行卡号
    @staticmethod
    def get_bank_card():
        return fake.credit_card_number()

    # 3、电子邮件
    @staticmethod
    def get_email():
        return fake.email()

    # 4、企业名称
    @staticmethod
    def get_company_name():
        list_temp = ['公司', '店', '厂', '院', '有限公司', '有限责任公司']
        first = fake.address()[:7]
        second = fake.company()[:4]
        third = random.choice(list_temp)
        company_name = first + second + third
        return company_name

    @staticmethod
    def get_company():
        list_temp = ['公司', '店', '厂', '院', '有限公司', '有限责任公司']
        first = fake.address()[:7]
        second = fake.company()[:4]
        third = random.choice(list_temp)
        company_name = first + second + third
        return company_name

    # 5、中文姓名
    @staticmethod
    def get_name():
        return fake.name()

    @staticmethod
    def get_name1():
        list1 = ['', fake.name()]
        return random.choice(list1)

    # 6、身份证
    @staticmethod
    def get_id_no():
        return fake.ssn()

    @staticmethod
    def get_id_card():
        return fake.ssn()

    # 7、电话
    @staticmethod
    def get_phone():
        return fake.phone_number()

    @staticmethod
    def get_phone_number():
        return fake.phone_number()

    @staticmethod
    def get_fix_phone():
        return fake.phone_number()

    # 8、邮政编码
    @staticmethod
    def get_post_code():
        return fake.postcode()

    # 9、车牌号码fake.license_plate()
    @staticmethod
    def get_car_no():
        list1 = ['京', '津', '冀', '晋', '内', '辽', '吉', '黑', '沪', '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤', '桂', '琼', '渝', '川', '黔', '滇', '藏', '陕', '甘', '青', '宁', '新', '港', '澳', '台', '军', '使', 'WJ']
        list2 = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        list3 = ['0', '1', '2', '3', '4', '6','7', '8', '9']
        exp_str = random.choice(list1) + random.choice(list2) + ''.join(random.sample(list3,5))
        return exp_str

    # 10、社会信用账号 @最后一位
    @classmethod
    def get_social_credit_code(cls):
        dict_temp1 = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'J': 18, 'K': 19, 'L': 20, 'M': 21,
            'N': 22, 'P': 23, 'Q': 24,
            'R': 25, 'T': 26, 'U': 27, 'W': 28, 'X': 29, 'Y': 30}
        code = cls.get_number(16)
        code = cls.create_c9(code[:16])
        # 第i位置上的加权因子
        weighting_factor = [1, 3, 9, 27, 19, 26, 16,
                            17, 20, 29, 25, 13, 8, 24, 10, 30, 28]
        # 本体代码
        ontology_code = code[0:17]
        # 计算校验码
        tmp_check_code = cls.gen_check_code(
            weighting_factor, ontology_code, 31, dict_temp1)
        return code[:17] + tmp_check_code

    @classmethod
    def create_c9(cls, code):
        dict_temp2 = {
            '0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9,
            'A': 10, 'B': 11, 'C': 12, 'D': 13, 'E': 14, 'F': 15, 'G': 16, 'H': 17, 'I': 18, 'J': 19, 'K': 20, 'L': 21,
            'M': 22, 'N': 23, 'O': 24, 'P': 25, 'Q': 26,
            'R': 27, 'S': 28, 'T': 29, 'U': 30, 'V': 31, 'W': 32, 'X': 33, 'Y': 34, 'Z': 35}
        # 第i位置上的加权因子
        weighting_factor = [3, 7, 9, 10, 5, 8, 4, 2]
        # 第9~17位为主体标识码(组织机构代码)
        organization_code = code[8:17]
        # 本体代码
        ontology_code = organization_code[0:8]
        # 生成校验码
        tmp_check_code = cls.gen_check_code(
            weighting_factor, ontology_code, 11, dict_temp2)
        return code[:16] + tmp_check_code

    @staticmethod
    def gen_check_code(weighting_factor, ontology_code, modulus, check_code_dict):
        total = 0
        for i in range(len(ontology_code)):
            if ontology_code[i].isdigit():
                total += int(ontology_code[i]) * weighting_factor[i]
            else:
                total += check_code_dict[ontology_code[i]
                         ] * weighting_factor[i]
        C9 = modulus - total % modulus
        C9 = 0 if C9 == 31 else C9
        C9 = list(check_code_dict.keys())[
            list(check_code_dict.values()).index(C9)]
        return C9

    # 11、汽车车架号
    @staticmethod
    def get_car_code():
        list1 = ['0', '1', '2', '3', '4', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'J', 'K', 'L',
                 'M', 'N', 'P', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
        list2 = [0, 1, 2, 3, 4, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 1, 2, 3, 4, 5, 7, 9, 2, 3, 4, 5, 6, 7, 8, 9]
        list3 = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17]
        list4 = [8, 7, 6, 5, 4, 3, 2, 10, 1, 9, 8, 7, 6, 5, 4, 3, 2]
        dict_tar1 = dict(zip(list1, list2))
        dict_tar2 = dict(zip(list3, list4))
        car_code_list = random.sample(list1, 17)

        sum = 0
        copy_list = car_code_list.copy()
        for char in copy_list:
            if copy_list.index(char) != 8:
                num1 = dict_tar1[char]
                num2 = dict_tar2[copy_list.index(char)+1]
                sum += num1*num2
                copy_list[copy_list.index(char)] = "*"
        if sum % 11 == 10:
            tar_char = 'X'
        else:
            tar_char = sum % 11
        car_code_list[8] = str(tar_char)
        car_code = ''.join(car_code_list)
        return car_code

    # 12、护照
    @staticmethod
    def get_passport():
        list1 = ['14', '15', 'G', 'P', 'S', 'D']
        list2 = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        first = random.choice(list1)
        passport = first + ''.join(random.sample(list2, (9-len(first))))
        return passport

    # 13、税务登记证号
    @staticmethod
    def get_tax_code():
        list1 = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        last = ''.join(random.sample(list1, 2))
        return str(fake.ssn()) + last

    # 14、组织机构代码
    @staticmethod
    def get_organization():
        ww = [3, 7, 9, 10, 5, 8, 4, 2]
        cc = []
        dd = 0
        for i in range(8):
            cc.append(random.randint(1, 9))
            dd = dd + cc[i] * ww[i]
        for i in range(len(cc)):
            cc[i] = str(cc[i])
        C9 = 11 - dd % 11
        if C9 == 10:
            C9 = 'X'
        else:
            if C9 == 11:
                C9 = ''
            else:
                C9 = str(C9)
        cc.append('-' + C9)
        return "".join(cc)

    # 15、营业执照代码
    @staticmethod
    def get_enterprise_code():
        list1 = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        list2 = ['1', '2', '3', '4', '6', '7']
        first = random.choice(list2)
        second = ''.join(random.sample(list1, 5))
        third = '6'
        fourth = ''.join(random.sample(list1, 7))
        # 查不到校验规则，暂时搁置
        end = random.choice(list1)
        code = first + second + third + fourth + end
        return code

    # 16、单体商户名称
    @staticmethod
    def get_individual_business():
        list1 = ['商行', '庄', '部', '厂', '店', '坊', '室', '场', '美发沙龙店', '烟花爆竹店', '美容美体店', '酸辣粉店', '酸菜鱼馆', '麻辣烫店', '缝纫机店', '私房菜馆', '农家菜馆', '五金电机', '商业银行', '股份银行', '手工编织', '羊毛衫厂', '美发天地', '木业经营']
        company = fake.company().replace('有限公司','')
        shop = company + random.choice(list1)
        return shop

    # 17、军官警官证编号
    @staticmethod
    def get_officer_card():
        list1 = ['军', '兵', '士', '文', '职', '军离', '军退', '武', '武离', '武退', '南', '北', '沈', '兰', '成', '济', '广', '参', '证', '后', '装', '海', '空']
        list2 = ['0', '1', '2', '3', '4', '6', '7', '8', '9']
        card = random.choice(list1) + '字第' + ''.join(random.sample(list2,7)) + '号'
        return card

#############################其他常见类型###########################################

    # 1、随机整数-可变长整数-限制长度50以内
    @staticmethod
    def get_number(length=None):
        if length:
            list1 = [str(i) for i in range(1, 10)] * 5
            str_num = ''.join(random.sample(list1, length))
            return str_num
        else:
            return random.randint(1, 10000)

    # 2、随机-或指定长度-字符串
    @staticmethod
    def get_character(length=None):
        if length:
            return fake.pystr(min_chars=None, max_chars=length)
        else:
            return fake.pystr(min_chars=None, max_chars=None)

    # 3、文章--限制长度500以内
    @staticmethod
    def get_description(length=None):
        if length:
            long = fake.paragraph(nb_sentences=100, variable_nb_sentences=True, ext_word_list=None)
            return long[:length]
        else:
            long = fake.paragraph(nb_sentences=3, variable_nb_sentences=True, ext_word_list=None)
            return long

    # 6、文章-含换行符
    @staticmethod
    def get_change_line_description():
        return fake.text(max_nb_chars=50, ext_word_list=None).replace('.','\n')

    # 7、时间-创建时间
    @staticmethod
    def get_create_time():
        time1 = str(datetime.datetime.now()).split('.')[0]
        return time1

    # 8、时间-更新时间
    @staticmethod
    def get_update_time():
        time1 = str(datetime.datetime.now()).split('.')[0]
        return time1

    # 9、时间-时间戳
    @staticmethod
    def get_timestamp():
        return str(time.time()*1000).split('.')[0]

    # 职位
    @staticmethod
    def get_job():
        return fake.job()

    # 完整信用卡信息
    @staticmethod
    def get_full_credit_card():
        return fake.credit_card_full(card_type=None)

    # 年月日
    @staticmethod
    def get_date():
        return fake.date(pattern="%Y-%m-%d", end_datetime=None)

    # 年
    @staticmethod
    def get_year():
        return fake.year()
        # return 1963

    # 月
    @staticmethod
    def get_month():
        return fake.month()

    # 日
    @staticmethod
    def get_day():
        return fake.day_of_month()

    # 周几
    @staticmethod
    def get_weekday():
        return fake.day_of_week()

    # 时间 时分秒
    @staticmethod
    def get_time():
        return fake.time(pattern="%H:%M:%S", end_datetime=None)

    # 时区
    @staticmethod
    def get_timezone():
        return fake.timezone()

    # 国家名称
    @staticmethod
    def get_country():
        return fake.country()

    # 省份
    @staticmethod
    def get_province():
        return fake.province()

    # 街道
    @staticmethod
    def get_street():
        return fake.street_address()

    # 颜色名称
    @staticmethod
    def get_color():
        return fake.color_name()

    # 颜色十六进制值
    @staticmethod
    def get_hex_color():
        return fake.hex_color()

    # 颜色十六进制值
    @staticmethod
    def get_file_name():
        return fake.file_name()

    # 文件路径
    @staticmethod
    def get_file_path():
        return fake.file_path(depth=3, category=None, extension=None)

    # 主机名
    @staticmethod
    def get_hostname():
        return fake.hostname(*args, **kwargs)

    # url
    @staticmethod
    def get_url():
        return fake.url(schemes=None)

    # 图片url
    @staticmethod
    def get_image_url():
        return fake.image_url(width=None, height=None)

    # ipv4
    @staticmethod
    def get_ipv4():
        return fake.ipv4(network=False, address_class=None, private=None)

    # ipv6
    @staticmethod
    def get_ipv6():
        return fake.ipv6(network=False)

    # mac
    @staticmethod
    def get_mac_address():
        return fake.mac_address()

    # 用户名
    @staticmethod
    def get_user_name():
        return fake.user_name(*args, **kwargs)

    # 二进制--暂固定20位
    @staticmethod
    def get_binary():
        return fake.binary(length=20)

    # 布尔值
    @staticmethod
    def get_boolean():
        return fake.boolean(chance_of_getting_true=50)

    # NULL+布尔值
    @staticmethod
    def get_null_boolean():
        return fake.null_boolean()

    # 密码
    @staticmethod
    def get_password():
        return fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)

    # md5
    @staticmethod
    def get_md5():
        return fake.md5(raw_output=False)

    # sha1
    @staticmethod
    def get_sha1():
        return fake.sha1(raw_output=False)

    # sha256
    @staticmethod
    def get_sha256():
        return fake.sha256(raw_output=False)

    # 档案(完整)--字典
    @staticmethod
    def get_profile():
        return fake.profile(fields=None, sex=None)

    # 档案(简单)--字典
    @staticmethod
    def get_simple_profile():
        return fake.simple_profile(sex=None)

    # 字典
    @staticmethod
    def get_dictionary():
        return fake.pydict(nb_elements=5, variable_nb_elements=True)

    # 列表
    @staticmethod
    def get_list():
        return fake.pylist(nb_elements=5, variable_nb_elements=True)

    # 集合
    @staticmethod
    def get_set():
        return fake.pyset(nb_elements=5, variable_nb_elements=True)

    # 元组
    @staticmethod
    def get_tuple():
        return fake.pytuple(nb_elements=5, variable_nb_elements=True)

    # 嵌套结构数据
    @staticmethod
    def get_struct():
        return fake.pystruct(count=10)

    # 几位小数--小于等于14
    @staticmethod
    def get_float(length=None):
        if length:
            if int(length) > 14:
                print("wrong length: it should be smaller than 15...")
            return fake.pyfloat(left_digits=None, right_digits=length, positive=True, min_value=None, max_value=None)
        else:
            return fake.pyfloat(left_digits=None, right_digits=None, positive=True, min_value=None, max_value=None)

    # 随机浏览器代理信息
    @staticmethod
    def get_user_agent():
        return fake.user_agent()

    # 特殊字符串--长度小于22-list长度；
    @staticmethod
    def get_special_character(length=None):
        list_temp = ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '<', '>', '?', '|', '.', '-', '_', ',', '/']
        if length:
            str_num = ''.join(random.sample(list_temp, length))
            return str_num
        else:
            str_num = ''.join(random.sample(list_temp, 7))
            return str_num

    # 011、少数民族姓名
    @staticmethod
    def get_special_name():
        list_temp = ['阿衣努尔·阿依古丽', '巴合提古丽·叶尔木拉提', '叶尔阿斯力·如娜仁', '吉日嘎拉·敖登格日乐', '巴雅尔', '乌日塔那顺', '迪丽热巴·迪力木拉提']
        return random.choice(list_temp)

    @staticmethod
    def get_uuid():
        return fake.uuid4()

###################### 固定正则匹配数据 ############################

    # 正则一、

    # 正则二、

    # 正则三、

######################## 非隐私类型 ####################################

    # 1、空值
    @staticmethod
    def get_null_value1():
        return 'null'

    @staticmethod
    def get_null_value2():
        return ''

    @staticmethod
    def get_null_value3():
        return ' '

    # 2、其他
    @staticmethod
    def get_uuid():
        return fake.uuid4()

    @classmethod
    def get_uid(cls):
        return cls.get_number(7)

##########################  ############################


fake.add_provider(MyProvider)


base_list1 = ['address', 'bank_card', 'email', 'company_name', 'enterprise_name', 'name', 'id_no', 'id_card', 'phone', 'phone_number', 'fix_phone', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code', 'organization', 'enterprise_code', 'individual_business', 'officer_card']

class MockMysqlData:

    @staticmethod
    # 生成获取columns的mysql语句
    def get_columns(dbname, table_name):
        sql0 = """SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{dbname}' AND TABLE_NAME = '{table_name}';""".format(dbname=dbname, table_name=table_name)
        return sql0

    @staticmethod
    # 生成单条sql插入的语句
    def single_sql(table_name, column_list):
        data1 = [getattr(fake, ('get_'+i.lower()))() for i in column_list]
        col1 = ','.join(column_list)
        new_col = '(' + col1 + ')'
        sql1 = "insert into {table_name} {columns} values {sql_data};".format(table_name=table_name, columns=new_col, sql_data=tuple(data1))
        return sql1

    @staticmethod
    def many_sql(table_name, column_list, number, start_index):
        data_list = []
        for i in range(int(number)):
            data1 = [getattr(fake, ('get_'+j.lower()))() for j in column_list]
            data1[0] = i + int(start_index) + 1
            data_list.append(tuple(data1))
        values_format = '%s'
        for i in range(len(column_list)-1):
            values_format += ',%s'
        values_format = '('+values_format+')'
        columns_format = '('+','.join(column_list)+')'
        sql2 = "insert into {table_name} {columns} values {values_format}".format(table_name=table_name, columns=columns_format, values_format=values_format)
        return [sql2, data_list]

    # 暂未测试
    @staticmethod
    def load_file_data(table_name, column_list, numbers):
        col1 = ','.join(column_list)
        new_col = '(' + col1 + ')'
        sql3 = "load data infile '{file_path}' into table {table_name} {columns};".format(file_path='./data.txt', table_name=table_name, columns=new_col)
        with open(r'./data.txt', 'w+') as f:
            for i in range(int(numbers)):
                data1 = [getattr(fake, i)() for i in column_list]
                data1[0] = i + 102
                new_data1 = (str(tuple(data1))).strip('(').strip(')')
                f.write(new_data1+'\n')
        return sql3


class MockOracleData:

    @staticmethod
    def insert_one_contains_index(table_name, columns_list, start_index):
        data1 = [getattr(fake, ('get_'+j.lower()))() for j in columns_list]
        data1[0] = int(start_index) + 1
        col1 = ','.join(columns_list)
        new_col = '(' + col1 + ')'
        sql1 = "insert into {table_name} {columns} values {values_format}".format(table_name=table_name, columns=new_col, values_format=tuple(data1))
        return sql1

    @staticmethod
    def insert_one(table_name, columns_list):
        data1 = [getattr(fake, ('get_'+j.lower()))() for j in columns_list]
        col1 = ','.join(columns_list)
        new_col = '(' + col1 + ')'
        sql1 = "insert into {table_name} {columns} values {values_format}".format(table_name=table_name, columns=new_col, values_format=tuple(data1))
        return sql1

    @staticmethod
    def insert_many(table_name, columns_list, start_index, number):
        columns_format = '(' + ','.join(columns_list) + ')'
        sql2 = "insert all"
        for i in range(int(number)):
            data1 = [getattr(fake, ('get_'+j.lower()))() for j in columns_list]
            data1[0] = int(start_index) + 1 + i
            sql2 += '\n'
            sql2 += "into {table_name} {columns_format}  values {value}".format(table_name=table_name, columns_format=columns_format, value=tuple(data1))
        sql2 += '\n'
        sql2 += "SELECT 1 from dual"

        return sql2

    @staticmethod
    def get_columns(table_name):
        sql001 = "SELECT wm_concat(T.COLUMN_NAME) as cols FROM USER_TAB_COLUMNS T WHERE T.TABLE_NAME = '{}'".format(table_name)
        return sql001

    @staticmethod
    def one_column_data(column_name, number):
        data_list = []
        for i in range(number):
            new_data = getattr(fake, column_name)
            data_list.append(new_data)
        return data_list


# hive-这里不能带';'
class MockMyhiveData:

    @staticmethod
    # 生成获取columns的mysql语句
    def get_columns(dbname, table_name):
        sql0 = """SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_SCHEMA = '{dbname}' AND TABLE_NAME = '{table_name}'""".format(dbname=dbname, table_name=table_name)
        return sql0

    @staticmethod
    # 生成单条sql插入的语句
    def single_sql(table_name, column_list):
        data1 = [getattr(fake, ('get_'+i.lower()))() for i in column_list]
        col1 = ','.join(column_list)
        new_col = '(' + col1 + ')'
        sql1 = "insert into {table_name} {columns} values {sql_data}".format(table_name=table_name, columns=new_col, sql_data=tuple(data1))
        return sql1


if __name__ == '__main__':
    # 1、新建mock
    # new_mock = MockMyhiveData()
    new_mock = MockOracleData()

    # 2、新建连接
    # new_presto_connect = MySql(host='192.168.7.240',sql_type='presto')
    new_oracle_connect = MySql(host='192.168.9.215', port=1521, user='TESTOR', passwd='123456', sample='XE', sql_type='oracle')
    # new_mysql_connect = MySql(host='192.168.7.241', port=3306, user='root', passwd='123456', dbname='autotest1', sql_type='mysql')

    # 3、提供表名 和 列
    table_name = 'autotest1.all_private_table3'
    column_list_new = ['uuid', 'name', 'phone_number', 'id_no', 'address', 'bank_card', 'company_name', 'job', 'email', 'post_code', 'car_no', 'social_credit_code', 'car_code', 'passport', 'tax_code', 'organization', 'enterprise_code', 'individual_business', 'officer_card']
    # column_list_new = ['uuid','name','name1','address','phone','company']
    # # 4-1、只造数据、写入文件
    # with open(r'sql_temp001','w',encoding='utf-8') as f:
    #     for i in range(10):
    #         sql001 = new_mock.single_sql(table_name=table_name, column_list=column_list_new)
    #         f.write(sql001.replace('\u2022','')+'\n')

    # 4-2、直接连接sql并插入数据
    t1 = time.time()
    for i in range(1000):
        sql001 = new_mock.single_sql(table_name=table_name, column_list=column_list_new)
        new_presto_connect.get_data_hive(sql001)
        # new_presto_connect.execute_sql(sql001)
        new_presto_connect.commit()
    t2 = time.time()

    # # 5、末尾-关闭连接
    new_presto_connect.close()
    print(t2-t1)


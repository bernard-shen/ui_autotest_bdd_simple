#!/usr/bin/python
# -*- coding: UTF-8 -*-
# --Author: Bernard--

# 用户登录
data001 = {
    "username": "autotest001",
    "password": "Mg4mp2R+crSHoPn5DkLy39o4WxzMWyVRFCMhdnyUWwEIBW4yyxhlxFw2e+r/O/HwvJrkaRysmDE88kpswAlgMA==",
    "realmFlag": "0"
}

# 新建数据连接参数
new_connection = {
    "connectInfo": {
        "aliasName": "shen-api-test68",
        "connectionType": 1,
        "dbSource": "0",
        "dataSourceType": "Mysql",
        "enableQuote": 1,
        "host": "192.168.7.241",
        "port": 3306,
        "dbName": "",
        "userName": "root",
        "password": "AtE0p3FEYNaC76b5+pK00Cj372HgAY+Q32pJrmA2NEjle9fJlkByW2c0Sczhqdo02nVKI1xiMOfk5PRJDSFjSSMd+vioQ61BeJXwSdfeuzZaXJ2fz9YPgPiothhfG9nUD11ygQnsTeGVPtUmuBc1MGFtg5zOf/iWum32u3DVIoZ491fvx/5LJRCFgfMTUnJlasd+Tor7sQ+dt83l+rpfgCGMk+qB8NKUNPqFDf8VN4Fj9mO7ax1IV/pAeAI+YZmxN+Y6tizLoCbE9OLz7g1m0B6KPIVW+QQ1kcBmIXWVlpS235DYWGsTY8mbsqQAQr0sXYIuRKzhK9CrU71P5XZZoA==",
        "status": "",
        "conAuthType": 1,
        "dbParams": "{}",
        "additionColumn": "{\"planUuid\":\"\",\"automaticTestConnectFlag\":\"1\",\"testConnectSchedule\":\"{\\\"type\\\":\\\"4\\\",\\\"time\\\":\\\"1\\\"}\",\"useFileLoadMode\":false,\"dbSource\":\"0\"}",
        "connectParams": "{}"
    },
    "taskInfo": {
        "discoverRangeType": 1,
        "selectedRange": [],
        "discoverPlanId": "initplan",
        "schedule": "",
        "option": "{\"objectTypes\":[\"3\"]}"
    }
}

# 新建时-尚不存在对应连接时-测试数据连接
test_connect_do_not_exist = {
    "aliasName": "shen-api-test111",
    "connectionType": 1,
    "dbSource": "0",
    "dataSourceType": "Mysql",
    "enableQuote": 1,
    "host": "192.168.7.241",
    "port": 3306,
    "dbName": "",
    "userName": "root",
    "password": "WmSEJelciDCj69wpZcTVthz9Ti30CRlDipwvqROMX6ziIO1YhNmH1ofVLR7kkkAV3psTbehaO9mZLTaNY8wVD81v7ruRlX2TFMcuUmqfmxpyukeIFXlTljQMvla7oQyHVb8H8Asq8HDAM0HL5XE1E/RAJY8jMs0k45KjyInfrLu5UEWuXU1EeVQMQftRERdzbuJOh8pcgfUPQyJSuvRuoCMDaNw6hZ+eVZwQCavxdxAWBAutHiWTxc7oBu5S3yYISq0dNOwRieEfBwG8jm4b6LLTG88FSyeQbDVPT8rUgg73SIKM5OJYh4J33SCY83+QWrX5jNIZWRWJf6RWhxmcVA==",
    "status": "",
    "conAuthType": 1,
    "dbParams": "{}",
    "additionColumn": "{'planUuid':'','automaticTestConnectFlag':'1','testConnectSchedule':'{'type':'4','time':'1'}','useFileLoadMode':False,'dbSource':'0'}",
    "connectParams": "{}"
}

# 查询数据连接列表
search_connection_list = {
    "aliasName": "shen",
    "dataSourceTypeArray": [],
    "dbSource": None,
    "createTime": [],
    "host": None,
    "port": None,
    "discoverStatusArray": [],
    "connectStatus": None,
    "status": None,
    "page": 1,
    "limit": 10
}

# 删除数据连接
del_connection = ["22023011100002859319"]

# 重新隐私发现, task_type 1:创建发现/2：手工重新发现/3：定时自动发现; incrementFlag 是否增量发现 1-是 0-否
re_discover = {
    "connectInfo": {
        "id": "22023011100002859294"
    },
    "taskInfo": {
        "incrementFlag": 1,
        "taskType": "2"
    }
}

# 隐私发现-字段隐私-列表查询
search_column_secret_list = {
    "aliasName": {
        "operateType": "1",
        "value": "SHEN-mysql666"
    },
    "schema": {
        "operateType": "1",
        "value": "autotest1"
    },
    "tableName": {
        "operateType": "1",
        "value": "shen_temp"
    },
    "columnName": {
        "operateType": "0",
        "value": "CARNO"
    },
    "columnType": None,
    "privacyTypeIds": [],
    "manualModify": None,
    "isSenseData": None,
    "hasAlert": False,
    "encryptFlag": None,
    "encryptionAlgorithm": None,
    "keyLength": None,
    "keyPath": {
        "operateType": "1",
        "value": ""
    },
    "dependFlag": False,
    "isAccurate": False,
    "page": 1,
    "limit": 10,
    "encryptionServer": True,
    "startTime": None,
    "endTime": None
}

# 隐私发现-字段隐私-隐私统计
# get方法，无参数，直接在url后拼接数据连接的task_id即connect_id

# 隐私发现结果-字段隐私-修改字段隐私类型; idList：发现结果-数据连接中对应字段的-id；privacyTypeId--隐私类型页面--列表中隐私类型对应的id;
column_secret_update = {
    "idList": [
        1122314
    ],
    "privacyTypeId": 6
}

# 隐私发现-结构发现-列表查询
struct_find_search = {
    "connect": {
        "operateType": "1",
        "value": ""
    },
    "schema": {
        "operateType": "1",
        "value": ""
    },
    "table": {
        "operateType": "1",
        "value": ""
    },
    "type": None,
    "name": {
        "operateType": "1",
        "value": ""
    },
    "page": 1,
    "limit": 10
}

# 隐私发现-发现历史-列表查询
find_history_search = {
    "id": None,
    "aliasName": None,
    "discoverPlan": None,
    "incrementFlag": None,
    "taskType": None,
    "taskStatus": None,
    "startTime": None,
    "endTime": None,
    "page": 1,
    "limit": 10
}

# 隐私发现-发现历史-差异对比; version即为发现次数；
result_compare = {
    "taskId": "22023011100002859294",
    "versionBefore": 4,
    "versionAfter": 6
}

# 隐私发现-发现历史-本次变化；====同差异对比，拿本次的和上次的进行差异对比

# 隐私发现-发现历史-错误信息
# get方法，无参数，直接在url后拼接数据连接的task_id即connect_id

# 新增字段隐私
new_field_privacy = {
    "schemaName": "autotest1",
    "tableName": "sdfdd212",
    "fieldName": "column2",
    "privacyTypeId": 2,
    "isEffect": 1
}

# 新建隐私类型
new_secret_type = {
    "privacyName": "shen002",
    "privacyCode": "Empty",
    "isBuiltIn": 0,
    "isRedline": 0,
    "findRule": "",
    "remark": "",
    "suffix": "",
    "ruleType": 5
}

# 新建隐私方案 ; privacyFindType隐私发现类型，1为默认，0时按需发现隐私类型--privacyList；priorityType优先级类型，1为默认，0时自定义优先级--对应 identifyPriority
# 优先级顺序： 1234排列顺序分别为：系统内置-正则-字典-日期；优先级顺序为：字典>日期>正则>系统内置
new_secret_plan = {
    "name": "shen_temp003",
    "privacyFindType": 0,
    "priorityType": 0,
    "assignField": "[{'id':1,'datasource':'','schema':'','table':'','column':'column','privacyId':3,'show':True}]",
    "remark": "",
    "identifyPriority": "{'0':'1','1':'2','2':'3','6':'4'}",
    "privacyList": "[{'createUserId':1,'createTime':'2022-01-01 00:00:00','updateUserId':290,'updateTime':'2022-12-04 04:41:33','deptId':0,'id':1,'privacyName':'中文地址信息','privacyCode':'Address','findRule':None,'params':None,'isBuiltIn':1,'ruleType':0,'isRedline':0,'remark':'对中文地址类数据进行自动识别','appCode':None,'relevancePlanCount':None,'relevanceResultCount':None,'quoteRegister':None},{'createUserId':1,'createTime':'2022-01-01 00:00:00','updateUserId':164,'updateTime':'2022-12-04 05:04:22','deptId':0,'id':2,'privacyName':'银行卡号信息','privacyCode':'BankCard','findRule':None,'params':None,'isBuiltIn':1,'ruleType':0,'isRedline':0,'remark':'对银行卡号类数据进行自动识别','appCode':None,'relevancePlanCount':None,'relevanceResultCount':None,'quoteRegister':None}]"
}

# 隐私方案提交
secret_plan_submit = {
    "uuid": "22023012900003245372"
}

# 隐私方案审批
secret_plan_approve = {
    "uuid": "22023012900003245372",
    "status": 1,
    "approvalOpinion": ""
}
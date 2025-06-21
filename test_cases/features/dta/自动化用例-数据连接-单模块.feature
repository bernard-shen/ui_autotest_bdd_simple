Feature: <自动化用例-数据连接单模块>

  ##### 备注1：本模块可能因环境问题，可能会导致部分fail 和 block；需手动确认不同类型数据库连接是否可用；
  ##### 备注2：本模块建议非并发执行；
  ##### 备注3：需求更新--报错提示更精确了，比如之前的“连接失败”--现在则是具体的报错提示；
  Background: 前置条件-假设使用admin账户登录
    Given 已登录到DTA环境 "http://192.168.9.116"
    And 已成功进入数据连接页面
    And 页面左上角包含"新建连接"按钮


  @自动化测试  @数据连接
  Scenario: 用例1.验证"新建连接"按钮能否点击
    Given 已成功进入数据连接页面
    When 点击"新建连接"
    Then 进入新建连接页面


  @自动化测试  @数据连接
  Scenario: 用例2.验证新建连接页面布局是否正确
    Given 已进入新建连接页面
    When 点击"高级选项"
    Then 展开参数"是否为加密库"、"自定义参数"
    And 页面包含字段:"连接名称"、"数据源类型"、"子机构可用"、"IP地址"、"端口"、"连接模式"、"数据库名称"、"认证方式"、"用户名"、"密码"
    And 包含"测试连接"、"保存为草稿"、"保存"、"返回"按钮
#
#
#  @自动化测试  @数据连接
#  Scenario: 用例3.验证新建连接页面IP地址能否为空
#    Given 已进入新建连接页面
#    And 已填写任意连接名称[test不存在的连接1]
#    When IP地址内容输入为空
#    And 鼠标与输入框失去焦点时
#    And 点击"保存"
#    And 点击"保存"
#    Then IP地址输入框下方出现提示:[请输入内容]
#
#
#  @自动化测试  @数据连接
#  Scenario Outline: 用例4.验证新建连接页面连接名称输入非法内容
#    Given 已进入新建连接页面
#    When 输入连接名称1为<connect_name>
#    And 点击"保存"
#    Then 连接名称输入框下方出现提示:[只能输入中英文，数字，-和_]
#    Examples:
#      | connect_name |
#      | 测试@1         |
#      | 测试 1         |
#      | 测ceshi!12    |
#
#
#  @自动化测试  @数据连接
#  Scenario: 用例5.验证新建连接页面连接名称输入超过30个字符
#    Given 已进入新建连接页面
#    When 输入连接名称2为[1111111111111111111111111111111]
#    And 鼠标与输入框失去焦点时
#    Then 连接名称输入框下方出现提示:[最多输入30个字符]
#
#
#  @自动化测试  @数据连接
#  Scenario: 用例6.验证新建连接页面连接名称能否为空
#    Given 已进入新建连接页面
#    When 输入连接名称为空
#    And 鼠标与输入框失去焦点时
#    Then 连接名称输入框下方出现提示:[请输入内容]
#
#  @自动化测试  @数据连接
#  Scenario: 用例7.验证新建连接页面查看数据源类型是否匹配
#    Given 已进入新建连接页面
#    When 点击数据源类型下拉单选框
#    Then 包含下方数据源可选
#      | db_source  |
#      | Oracle     |
#      | Mysql      |
#      | IBM Db2    |
#      | Hive       |
#      | XHHive     |
#      | Postgresql |
#      | ClickHouse |
#      | HBase      |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例8.验证新建连接页面IP地址输入非法的IP地址
#    Given 已进入新建连接页面
#    When 输入下方的IP地址<ip>
#    And 鼠标与输入框失去焦点时
#    Then IP地址输入框下方出现提示:[请输入合法的IP地址或域名]
#    Examples:
#      | ip       |
#      | abc      |
#      | 123      |
#      | sbcqwe15 |
##
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例9.验证新建连接页面-自动测试连接失败修改后再次点击测试连接成功
#    Given 已进入新建连接页面
#    And 选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    When 点击测试连接
#    Then 系统提示:"连接失败"
#    When 修改password为[123456]
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    Examples:
#      | db_source  |  connect_name     | ip            | port  | db_name | username | password |
#      | Mysql      | SHEN-Mysql-tt1      | 192.168.7.241 | 3306  | testor  | root     | 123      |
#      | Postgresql | SHEN-Postgresql-tt1 | 192.168.7.240 | 5432  | testdb  | testor   | 123      |
#      | IBM Db2    | SHEN-DB2-tt1      | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123      |
#      | Oracle     | SHEN-Oracle-tt1    | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123      |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例10-验证新建连接页面-自动测试连接失败再次点击测试连接失败
#    Given 已进入新建连接页面
#    And 选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    When 点击测试连接
#    Then 系统提示:"连接失败"
#    When 点击测试连接
#    Then 系统提示:"连接失败"
#    Examples:
#      | db_source  | connect_name     | ip            | port  | db_name | username | password |
#      | Mysql      |   SHEN-Mysql-tt1      | 192.168.7.241 | 3306  | testor  | root     | 123      |
#      | Postgresql |   SHEN-Postgresql-tt1 | 192.168.7.240 | 5432  | testdb  | testor   | 123      |
#      | DB2        |   SHEN-DB2-tt1        | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123      |
#      | Oracle     | SHEN-Oracle-tt1    | 192.168.7.240 | 1521  | ORCL      | TESTOR   | 123      |
##
##
#   @自动化测试  @数据连接
#  Scenario Outline: 用例11.验证新建连接页面-自动测试连接成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    Examples:
#      | db_source  |  connect_name     | ip            | port  | db_name | username | password |
#      | Mysql      | SHEN-Mysql-tt1      | 192.168.7.241 | 3306  | testor  | root     | 123456   |
#      | Postgresql | SHEN-Postgresql-tt1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   |
#      | IBM Db2    | SHEN-DB2-tt1       | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   |
#      | Hive       | SHEN-Hive-tt1       | 192.168.7.242 | 10000 | default | hdfs     | 123456   |
#      | Gbase      | SHEN-Gbase-tt1      | 192.168.7.244 | 5258  | gbase   | root     | root     |
#      | Presto     | SHEN-Presto-tt1     | 192.168.7.240 | 8080  | hive    | hive     | NULL     |
#      | Oracle     | SHEN-Oracle-tt1     | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456      |
#      | ClickHouse | SHEN-ClickHouse-tt1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     |
#
#
#  #########网络超时也会保存为异常连接，但是页面弹出提示框内容不一致；
#   @自动化测试  @数据连接
#  Scenario Outline: 用例12.验证新建连接页面-自动测试连接失败保存能否保存为异常连接
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接失败1"
#    When 点击"保存"
#    ##此处保存时间较长，可以加一个等待
#    Then 页面弹出1提示框[已保存为异常连接，如需使用请修改连接信息]
#    And 列表新增一条连接名称为<connect_name>,连接状态为"异常"的数据
#    And 该连接隐私识别状态为"-"
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name     | ip            | port  | db_name | username | password |
#      | Mysql      | SHEN-Mysql-a1      | 192.168.7.241 | 3306  | testor  | root     | 123      |
##      | Postgresql | SHEN-Postgresql-a1 | 192.168.7.240 | 5432  | testdb  | testor   | 123      |
##      | IBM Db2    | SHEN-DB2-a1        | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123      |
##      | Hive       | SHEN-Hive-a1        | 192.168.7.241 | 10000 | default | hdfs     | 123      |
##      | Gbase      | SHEN-Gbase-a1    | 192.168.7.244 | 5258  | gbase   | root     | root123  |
##      | Oracle     | SHEN-Oracle-a1    | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123      |
##      | ClickHouse | SHEN-ClickHouse-a1 | 192.168.7.244 | 8133  | NULL    | NULL     | NULL     |
##
#   @自动化测试  @数据连接
#  Scenario: 用例13.验证新建连接页面-取消新增能否成功
#    Given 已进入新建连接页面
#    When 依次输入conn_name、ip、port、db_name、user、password
#      | conn_name      | ip            | port | db_name | username   | password |
#      | SHEN-Oracle_temp | 192.168.7.241 | 1526 | XE       | testor | 123      |
#    When 点击返回
#    Then 数据连接列表页,搜索[SHEN-Oracle_temp],连接不存在
##
#
#  @自动化测试  @数据连接
#  Scenario Outline: 用例14.验证新增全部数据连接-发现全部数据,能否新建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    When 点击"保存"
#    Then 新建连接成功,触发隐私发现
#    And 连接<connect_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name         | ip            | port  | db_name | username | password |
#      | Mysql      |  SHEN-Mysql-b1   | 192.168.7.241 | 3306  | testor  | root     | 123456   |
#      | Postgresql |   SHEN-Postgresql-b1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   |
#      | IBM Db2    |   SHEN-DB2-b1     | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   |
#      | Hive       |   SHEN-Hive-b1      | 192.168.7.242 | 10000 | default | hdfs     | 123456   |
#      | Gbase      |   SHEN-Gbase-b1       | 192.168.7.244 | 5258  | gbase   | root     | root     |
#      | Oracle     |   SHEN-Oracle-b1   | 192.168.7.240 | 1521  | ORCL     | TESTOR   | 123456   |
#      | Presto     |   SHEN-Presto-b1    | 192.168.7.240 | 8080  | hive    | hive     | NULL     |
#      | ClickHouse |   SHEN-ClickHouse-b1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例15.验证新增全部数据连接-发现部分数据,能否新建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    When 发现范围选择"发现部分",勾选<find_schema>
#    And 点击"保存"
#    Then 新建连接成功,触发隐私发现
#    And 连接<connect_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name          | ip           | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql-c1     | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-c1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-c1        | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-c1       | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-c1     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#      | ClickHouse |  SHEN-ClickHouse-c1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
#      | Oracle     |  SHEN-Oracle-c1     | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
#      | Gbase      |  SHEN-Gbase-c1      | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
#
###
#   @自动化测试  @数据连接
#  Scenario: 用例16.验证新建连接页面用户名能否为空
#    Given 已进入新建连接页面
#    When 依次输入conn_name、ip、port、db_name、user、password
#      | conn_name        |        ip     | port | db_name | username   | password |
#      | SHEN-Oracle-done | 192.168.7.240 | 1521 | ORCL    |            | 123      |
#    And 用户名输入为空
#    And 点击"保存"
#    Then 用户名输入框下方出现提示:[请输入内容]
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例17.验证新增数据连接-保存草稿能否成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<connect_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    When 点击保存草稿
#    Then 系统提示:"保存草稿成功"
#    And 列表新增一条连接名称为<connect_name>，数据源状态为"草稿"的数据
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name     | ip           | port  | db_name | username  | password |
#      | Oracle     | SHEN-Oracle-d1     | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   |
#      | Mysql      | SHEN-Mysql-d1      | 192.168.7.241 | 3306  | testor  | root     | 123456   |
#      | Postgresql | SHEN-Postgresql-d1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   |
#      | IBM Db2    | SHEN-DB2-d1       | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   |
#      | Hive       | SHEN-Hive-d1      | 192.168.7.242 | 10000 | default | hdfs     | 123456   |
#      | Gbase      | SHEN-Gbase-d1     | 192.168.7.244 | 5258  | gbase   | root     | root     |
#      | Presto     | SHEN-Presto-d1     | 192.168.7.240 | 8080  | hive    | hive     | NULL     |
#      | ClickHouse | SHEN-ClickHouse-d1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     |
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例18.验证新建连接页面连接名称是否重复
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入新建连接页面
#    When 输入已存在的连接名称[SHEN-Mysql3]
#    And 鼠标与输入框失去焦点时
#    Then 连接名称输入框下方出现提示:[名称重复]
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例19.验证新建连接页面-数据源类型为Oracle,输入不合法的数据库名称
#    Given 已进入新建连接页面
#    When 数据源库类型选择"Oracle"
#    And 数据库名称输入[X E]
#    And 鼠标与输入框失去焦点时
#    Then 数据库名称输入框下方出现提示:[仅可输入英文字母、数字、“-”、“_”]
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例20.验证新建连接页面-数据库名称能否为空
#    Given 已进入新建连接页面
#    When 数据源库类型选择"Oracle"
#    And 数据库名称输入为空
#    And 点击测试连接
#    Then 数据库名称输入框下方出现提示:[请输入内容]
#
#################################################
##
# @自动化测试  @数据连接
#  Scenario: 用例21.验证复制连接能否点击
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    When 选择已存在的连接[SHEN-Mysql3],点击"复制"
#    Then 进入复制连接页面
#    And 页面包含字段:"连接名称"、"数据源类型"、"子机构可用"、"IP地址"、"端口"、"认证方式"、"用户名"、"密码"
#    When 回到数据连接列表页面
#    Then 搜索和删除对应数据连接[SHEN-Mysql3]成功
#
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例22.验证复制连接页面-连接名称是否不能重复
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入存在的连接名称A
#    And 点击"保存"
#    Then 连接名称输入框下方出现提示:[名称重复]
#
#   @自动化测试  @数据连接
#  Scenario: 用例23.验证复制连接页面-连接名称能否为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入为空
#    And 点击"保存"
#    Then 连接名称输入框下方出现提示:[请输入内容]
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例24.验证复制连接页面-查看数据源类型是否匹配
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 点击数据源类型下拉单选框
#    Then 包含下方数据源可选
#      | db_source  |
#      | Oracle     |
#      | Mysql      |
#      | IBM Db2    |
#      | Hive       |
#      | XHHive     |
#      | Postgresql |
#      | ClickHouse |
#      | HBase      |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例25.验证复制连接-选择发现全部数据-是否成功
#    Given 列表存在数据连接<conn_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>新建
#    And 已进入该连接的复制页面
#    When 连接名称填入<conn_name_copy1>,用户名填入<username>,密码填入<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    Then 页面下方显示"隐私发现任务参数"部分
#    When 点击"保存"
#    Then 保存成功,回到数据连接页面,页面新增一条<conn_name_copy1>的数据连接
#    When 等待数据连接<conn_name_copy1>-隐私发现完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name_copy1>成功
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name>成功
#    Examples:
#      | db_source  |  conn_name          | ip            | port  | db_name | username | password | conn_name_copy1 |
#      | Mysql      |  SHEN-Mysql-b1      | 192.168.7.241 | 3306  | testor  | root     | 123456   |  SHEN-Mysql-f1      |
#      | Postgresql |   SHEN-Postgresql-b1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   |  SHEN-Postgresql-f1 |
#      | IBM Db2    |   SHEN-DB2-b1       | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   |    SHEN-DB2-f1       |
#      | Hive       |   SHEN-Hive-b1      | 192.168.7.242 | 10000 | default | hdfs     | 123456   |   SHEN-Hive-f1       |
#      | Gbase      |   SHEN-Gbase-b1     | 192.168.7.244 | 5258  | gbase   | root     | root     | SHEN-Gbase-f1  |
#      | Oracle     |   SHEN-Oracle-b1    | 192.168.7.240 | 1521  | ORCL     | TESTOR   | 123456   |  SHEN-Oracle-f1  |
#      | Presto     |   SHEN-Presto-b1    | 192.168.7.240 | 8080  | hive    | hive     | NULL     | SHEN-Presto-f1   |
#      | ClickHouse |   SHEN-ClickHouse-b1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | SHEN-ClickHouse-f1 |
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例26.验证复制连接-选择发现部分数据-是否成功
#    Given 已经存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>,<find_schema>新建
#    And 已进入该连接的复制页面
#    When 连接名称填入<connect_name_copy2>,用户名填入<username>,密码填入<password>
#    And 点击"连接信息"
#    Then 系统提示:"连接成功"
#    Then 页面下方显示"隐私发现任务参数"部分
#    When 选择发现范围<find_schema>
#    And 点击"保存"
#    Then 保存成功,回到数据连接页面,页面新增一条<connect_name_copy2>的数据连接
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name_copy2>成功
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name   | connect_name_copy2  | ip           | port  | db_name | username  | password | find_schema |
#      | Mysql      |  SHEN-Mysql-c1  | SHEN-Mysql-g1       | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-c1 | SHEN-Postgresql-g1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-c1        | SHEN-DB2-g1      | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-c1      |SHEN-Hive-g1       | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-c1    | SHEN-Presto-g1    | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#      | ClickHouse |  SHEN-ClickHouse-c1 | SHEN-ClickHouse-g1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
#      | Oracle     |  SHEN-Oracle-c1    | SHEN-Oracle-g1    | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
#      | Gbase      |  SHEN-Gbase-c1     | SHEN-Gbase-g1     | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
##
#   @自动化测试  @数据连接
#  Scenario Outline: 用例27.验证复制连接-保存草稿能否成功
#    Given 已经存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>,<find_schema>新建
#    And 已进入该连接的复制页面
#    When 仅填入连接名称<connect_name_copy3>
#    And 点击"保存为草稿"
#    Then 列表新增一条名称为<connect_name_copy3>的数据连接
#    And 该连接数据源状态为[草稿]
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name_copy3>成功
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name   | connect_name_copy3  | ip           | port  | db_name | username  | password | find_schema |
#      | Mysql      |  SHEN-Mysql-c1  | SHEN-Mysql-g2       | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-c1 | SHEN-Postgresql-g2 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-c1        | SHEN-DB2-g2      | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-c1      |SHEN-Hive-g2       | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-c1    | SHEN-Presto-g2    | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#      | ClickHouse |  SHEN-ClickHouse-c1 | SHEN-ClickHouse-g2 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
#      | Oracle     |  SHEN-Oracle-c1    | SHEN-Oracle-g2    | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
#      | Gbase      |  SHEN-Gbase-c1     | SHEN-Gbase-g2     | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例28.验证复制连接页面-测试连接失败能否保存为异常连接
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 输入具体的连接名[YC-Oracle_temp],用户名[testor],密码[123]
#    And 点击测试连接
#    Then 系统提示:"连接失败"
#    When 点击"保存"连接
#    Then 连接页面新增一条数据源状态为"异常"的数据连接[YC-Oracle_temp]
#    When 回到数据连接列表页面
#    Then 搜索和删除对应数据连接[YC-Oracle_temp]成功
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例29.验证复制连接页面-密码能否为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入任意非重复名称[test_temp110],用户名输入[testor],密码输入为空
#    And 鼠标与输入框失去焦点时
#    Then 系统提示:"连接失败"
##
#   @自动化测试  @数据连接
#  Scenario: 用例30.验证复制连接页面-用户名能否为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入任意非重复名称[test1001],用户名输入为空
#    And 点击"保存"
#    Then 用户名输入框下方出现提示:[请输入内容]
#
#   @自动化测试  @数据连接
#  Scenario: 用例31.验证复制连接页面-修改连接参数,是否可以复制成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入任意非重复名称[SHEN-fuzhi1],修改ip为[192.168.7.248],用户名输入[testor],密码输入[123456],端口输入[49167]
#    And 点击"保存"
#    Then 保存成功
#    Then 页面新增一条名称为[SHEN-fuzhi1]的数据源
#    When 回到数据连接列表页面
#    Then 搜索和删除对应数据连接[SHEN-fuzhi1]成功
#
##
#   @自动化测试  @数据连接
#  Scenario: 用例32.验证复制连接页面-数据库名称能否为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Postgresql |  SHEN-Postgresql-3 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 连接名称输入任意非重复名称[SHEN-fuzhi2],修改数据库名称为空,用户名输入[testor],密码输入[123456]
#    And 点击"保存"
#    Then 数据库名称输入框下方出现提示:[请输入内容]
####
##
#   @自动化测试  @数据连接
#  Scenario: 用例33.验证复制连接-取消复制能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的复制页面
#    When 点击返回
#    Then 回到数据连接列表页面,搜索[SHEN-Mysql3]，仅有一条
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例34.验证新建连接-分别创建不同版本,不同编码,不同实例的Oracle数据连接,是否可以创建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<conn_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    When 发现范围选择"发现部分",勾选<find_schema>
#    And 点击"保存"
#    Then 新建连接成功,触发隐私发现,<conn_name>连接状态正常
#    And 连接<conn_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name>成功
#    Examples:
#      | db_source | conn_name        | ip            | port | db_name  | username   | password | find_schema |
#      | Oracle    | SHEN-Oracle11g-1 | 192.168.7.240 | 1521 | ORCL     | TESTOR | 123456   | TESTOR      |
#      | Oracle    | SHEN-Oracle11g-2 | 192.168.7.248 | 1525 | XE     | testor | TEST10G   | autotest1   |
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例35.验证新建连接-分别创建不同版本,不同编码,不同实例的Mysql数据连接,是否可以创建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<conn_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    And 页面下方显示"隐私发现任务参数"部分
#    When 发现范围选择"发现部分",勾选<find_schema>
#    And 点击"保存"
#    Then 新建连接成功,触发隐私发现,<conn_name>连接状态正常
#    And 连接<conn_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name>成功
#    Examples:
#      | db_source | conn_name         |db_name| ip            | port  | username | password | find_schema |
#      | Mysql     | SHEN-Mysql57-UTF |aa | 192.168.7.241 | 3306  | root | 123456   | autotest1   |
#      | Mysql     | SHEN-Mysql56     |aa | 192.168.7.240 | 49168 | root | 123456   | testdb      |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例36.验证新建连接-分别创建不同版本,不同实例的DB2数据连接,是否可以创建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<conn_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    Then 页面下方显示"隐私发现任务参数"部分
#    When 发现范围选择"发现部分",勾选<find_schema>
#    And 点击"保存"
#    Then 新建连接成功,触发隐私发现,<conn_name>连接状态正常
#    And 连接<conn_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name>成功
#    Examples:
#      | db_source | conn_name      | ip            | port  | db_name | username     | password     | find_schema |
#      | IBM Db2   | SHEN-DB2-V11-1 | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456       | autotest1   |
#      | IBM Db2   | SHEN-DB2-V10-5 | 192.168.7.244 | 50001 | SAMPLE  | db2inst1 | db2inst1-pwd | TESTDB      |
#      | IBM Db2   | SHEN-DB2-V11-5 | 192.168.7.241 | 50000 | testdb  | db2inst1 | 123456       | autotest1   |
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例37.验证新建连接-分别创建不同版本的PG数据连接,是否可以创建成功
#    Given 已进入新建连接页面
#    When 1选择数据源<db_source>,连接参数输入<conn_name>、<ip>、<port>、<db_name>、<username>、<password>
#    And 点击测试连接
#    Then 系统提示:"连接成功"
#    Then 页面下方显示"隐私发现任务参数"部分
#    When 发现范围选择"发现部分",勾选<find_schema>
#    And 点击"保存"
#    Then 新建连接成功,触发隐私发现,<conn_name>连接状态正常
#    And 连接<conn_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<conn_name>成功
#    Examples:
#      | db_source  | conn_name    | ip            | port | db_name | username     | password | find_schema |
#      | Postgresql | SHEN-PG-12-1 | 192.168.7.240 | 5432 | testdb  | testor   | 123456   | autotest1   |
#      | Postgresql | SHEN-PG-9-4  | 192.168.7.241 | 5432 | testdb  | postgres | 123456   | testdb      |
###
#   @自动化测试  @数据连接
#  Scenario: 用例38.验证修改连接-点击修改,是否进入修改连接页面
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    Then 页面包含字段:"连接名称"、"数据源类型"、"子机构可用"、"IP地址"、"端口"、"认证方式"、"用户名"、"密码"
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例39.验证修改连接-连接名称和数据源类型是否置灰不可修改
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When 鼠标移入连接名称输入框、数据源类型输入框
#    Then 置灰显示,不可点击
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例40.验证修改连接-IP地址是否不可为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When 修改IP地址输入框内容,输入为空
#    And 点击"保存"
#    And 点击"保存"
#    Then IP地址输入框下方出现提示:[请输入内容]
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例41.验证修改连接-IP地址是否不可输入非法内容
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When IP地址输入<ip>
#    And 点击"保存"
#    Then IP地址输入框下方出现提示:[请输入合法的IP地址或域名]
#    Examples:
#      | ip       |
#      | abc      |
#      | 123      |
#      | sbcqwe15 |
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例42.验证修改连接-数据库名称是否不可为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Postgresql |  SHEN-Postgresql-3 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When 修改数据库名称输入框内容,输入为空
#    And 点击"保存"
#    Then 数据库名称输入框下方出现提示:[请输入内容]
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例43.验证修改连接-用户名是否不可为空
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When 修改用户名输入框内容,输入为空
#    And 点击"保存"
#    Then 用户名输入框下方出现提示:[请输入内容]
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例44.验证修改连接-修改连接后,是否可以不进行隐私发现
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 该连接隐私识别状态为[完成]
#    And 已进入该连接的修改页面
#    When 修改该连接发现范围,增加一个schema[testor]
#    And 点击保存,"是否重新进行隐私发现"弹框中选择[不需要]
#    Then 回到数据连接列表页面
#    And 该连接连接状态为[正常],该连接隐私识别状态为[完成]
#
#
#  ### 实际上全量发现后，根据数据量的多或少，回到列表页，隐私识别的状态为运行或完成，所以这里会校验它的状态由运行最终变为完成
#   @自动化测试  @数据连接
#  Scenario Outline: 用例45.验证修改连接-新增schema,是否可以重新全量发现
#    Given 已经存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>,<find_schema>新建
#    And 该连接隐私识别状态为[完成]
#    And 已进入该连接的修改页面
#    When 修改发现范围,新增<find_schema1>
#    And 点击保存,"是否重新进行隐私发现"弹框中选择[全量发现]
#    Then 回到数据连接列表页面
#    And 该连接连接状态为[正常],隐私识别状态为[运行]或[完成]
#    And 连接<connect_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name         | find_schema1  | ip           | port  | db_name | username  | password | find_schema |
#      | Mysql      |  SHEN-Mysql-c1       | testdb      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-c1  | testdb      | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-c1         | TESTDB      | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-c1        | default     | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-c1      | default     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#      | ClickHouse |  SHEN-ClickHouse-c1  | T1          | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
#      | Oracle     |  SHEN-Oracle-c1      | TESTOR      | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
#      | Gbase      |  SHEN-Gbase-c1       | testdb      | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
##
###
###
#   @自动化测试  @数据连接
#  Scenario Outline: 用例47.验证修改连接-不修改任何内容,是否可以保存
#    Given 已经存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>,<find_schema>新建
#    And 该连接隐私识别状态为[完成]
#    And 已进入该连接的修改页面
#    When 点击保存,"是否重新进行隐私发现"弹框中选择[全量发现]
#    Then 回到数据连接列表页面
#    And 该连接连接状态为[正常],隐私识别状态为[运行]或[完成]
#    And 连接<connect_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name        |  ip           | port  | db_name | username  | password | find_schema |
#      | Mysql      |  SHEN-Mysql-e1       | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-e1  | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-e1         | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-e1        | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-e1      | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
##      | ClickHouse |  SHEN-ClickHouse-e1  | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
##      | Oracle     |  SHEN-Oracle-e1      | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
##      | Gbase      |  SHEN-Gbase-e1       | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
##
#
#   @自动化测试  @数据连接
#  Scenario: 用例48.验证修改连接-是否可以修改保存为异常连接
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql9   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 该连接隐私识别状态为[完成]
#    And 已进入该连接的修改页面
#    When 仅修改该连接IP地址为[192.168.7.2411]
#    And 点击保存,"是否重新进行隐私发现"弹框中选择[不需要]
#    #此处测试连接异常等待20秒
#    Then 页面弹出提示框[已保存为异常连接，如需使用请修改连接信息]
#    And 该数据连接,连接状态变为[异常]
#    When 回到数据连接列表页面
#    Then 搜索和删除对应数据连接[SHEN-Mysql9]成功
#
#
#  @自动化测试  @数据连接
#  Scenario: 用例49.验证修改连接-取消修改能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql4      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已进入该连接的修改页面
#    When 点击返回
#    Then 回到数据连接列表页面
#    And 该连接连接状态为[正常],该连接的隐私识别状态为[运行]或[完成]
#    When 回到数据连接列表页面
#    Then 搜索和删除对应数据连接[SHEN-Mysql4]成功
#
##
#   @自动化测试  @数据连接
#  Scenario: 用例50.验证删除连接-删除是否可点击
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    When 点击"更多-删除"
#    Then 弹出确认框,提示:"删除后不可找回，是否确定删除此连接?"
#
#
########################################################
#  ##此处数据连接单模块,故不考虑连接被任务关联的情况,默认没被关联
#  ## 隐私识别结束，包括：完成、失败、-；即非新建 和 运行；
#  @自动化测试  @数据连接
#  Scenario Outline: 用例51.验证删除连接-是否可以删除连接成功
#    Given 列表存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>新建
#    And 等待该连接隐私识别结束
#    When 点击"删除-确定"
#    Then 系统提示:"删除成功"
#    And 数据连接列表页,搜索<connect_name>,连接不存在
#    Examples:
#      | db_source  |  connect_name     | ip           | port  | db_name | username  | password |
#      | Mysql      |  SHEN-Mysql-b1   | 192.168.7.241 | 3306  | testor  | root     | 123456   |
#      | Oracle     |   SHEN-Oracle-b1   | 192.168.7.240 | 1521  | ORCL     | TESTOR   | 123456   |
#      | Postgresql |   SHEN-Postgresql-b1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   |
#      | IBM Db2    |   SHEN-DB2-b1     | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   |
#      | Hive       |   SHEN-Hive-b1      | 192.168.7.242 | 10000 | default | hdfs     | 123456   |
#      | Gbase      |   SHEN-Gbase-b1       | 192.168.7.244 | 5258  | gbase   | root     | root     |
#      | Presto     |   SHEN-Presto-b1    | 192.168.7.240 | 8080  | hive    | hive     | NULL     |
#      | ClickHouse |   SHEN-ClickHouse-b1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     |
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例52.验证删除连接-取消删除连接能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql3      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    When 点击"更多-删除"
#    And 点击"取消"
#    Then 回到数据连接列表页,该连接依然存在
###
##
#   @自动化测试  @数据连接
#  Scenario: 用例53.验证查询连接-查询不到数据时显示是否正确
#    Given 已成功进入数据连接页面
#    When 连接名称输入[SHEN999]
#    And 点击数据连接"查询"
#    Then 列表刷新,显示"暂无数据"
#
#
######  这里所有连接信息不太好校验和描述,目前是校验数据数量大于1
#  @自动化测试  @数据连接
#  Scenario: 用例54验证查询连接-查询条件重置能否成功
#    Given 已成功进入数据连接页面
#    When 连接名称输入[SHEN321]
#    And 点击数据连接"查询"
#    Then 列表刷新,显示"暂无数据"
#    When 点击"重置"
#    Then 列表刷新,返回至首页,显示所有连接信息
#    And 连接名称输入框内容为空
#
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例55.验证查询连接-查询能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql6      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    And 已成功进入数据连接页面
#    When 数据连接-等待[15]s
#    When 连接名称输入<conn_name>,数据源类型选择<db_source>,IP地址输入<ip>,端口输入<port>,连接状态输入<conn_status>,隐私识别状态选择<privacy_status>,创建日期选择<create_date>
#    And 点击数据连接"查询"
#    Then 查询成功,列表筛选出满足查询条件的数据<conn_name2>
#    Examples:
#      | conn_name    | db_source  | ip            | port  | conn_status | privacy_status | create_date           | conn_name2       |
#      | SHEN-My      | Mysql       | NULL          | NULL  | NULL       | NULL           | NULL                  | SHEN-Mysql6      |
#      | SHEN-Mysql6  | NULL       | NULL          | NULL  | NULL        | NULL           | NULL                  | SHEN-Mysql6      |
#      | SHEN-Mysql6   | Mysql      | 192.168.7.241 | 3306  | 正常        | 完成           | 2022-11-01~2023-12-01 | SHEN-Mysql6       |
#      | no_such_connection  | NULL | NULL       | NULL  | NULL          | NULL           | NULL                 | NULL      |
#
###
##
#   @自动化测试  @数据连接
#  Scenario: 用例56.验证数据连接页面-双击是否可查看连接信息
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 鼠标双击该连接名称
#    Then 弹出连接详情弹窗
#    And 包含字段:"连接名称"、"数据源类型"、"IP地址"、"端口"、"用户名"、"自定义参数"、"创建时间"、"创建人"、"连接状态"、"数据源状态"、"隐私识别状态"
#    And 字段:"连接名称"、"数据源类型"、"IP地址"、"端口"、"创建时间"、"连接状态"、"数据源状态"、"隐私识别状态"与连接列表统计内容一致
#
##
#   @自动化测试  @数据连接
#  Scenario: 用例57.验证数据连接页面-连接信息弹窗是否可以关闭
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 鼠标双击该连接名称
#    Then 弹出连接详情弹窗
#    When 点击"关闭"
#    Then 回到数据连接列表页面1
##
#   @自动化测试  @数据连接
#  Scenario: 用例58.验证数据连接页面-是否可以查看任务信息
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 点击该连接的"任务信息"
#    Then 弹出任务信息弹窗
#    And 弹窗左上角包含标题"隐私发现任务信息"
#    And 页面展示内容包含板块:"基本信息"、"隐私发现"、"隐私判定参数"、"任务运行参数"、"任务创建信息"
#
#   @自动化测试  @数据连接
#  Scenario: 用例59.验证数据连接页面-任务信息弹窗是否可以关闭
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 点击该连接的"任务信息"
#    Then 弹出任务信息弹窗
#    When 点击"关闭"
#    Then 回到数据连接列表页面
#
#   @自动化测试  @数据连接
#  Scenario: 用例60.验证数据连接页面-点击"识别结果"是否可以跳转
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 点击该连接的"发现结果"
#    Then 跳转到发现结果页面1
#    And 自动检索出连接名称为[SHEN-Presto-3]的发现结果
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例61.验证数据连接页面-是否可以点击"测试连接"
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    When 点击该连接的"测试连接"
#    Then 弹框提示:"连接成功"
##
#   @自动化测试  @数据连接
#  Scenario: 用例62.验证数据连接页面-数据源禁用能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    And 该连接数据源的状态为[启用]
#    When 点击"更多-禁用"
#    Then 弹框提示:"已禁用"
#    And 连接名称为[SHEN-Presto-3]的数据连接,数据源状态变更为[禁用]
#    When 点击"更多-启用"
#    Then 弹框提示:"已启用"
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例63.验证数据连接页面-数据源启用能否成功
#    Given 页面存在发现部分数据源的数据连接A,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      | Presto     |  SHEN-Presto-3     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#    And 该连接数据源的状态为[禁用]
#    When 点击"更多-启用"
#    Then 弹框提示:"已启用"
#    And 连接名称为[SHEN-Presto-3]的数据连接,数据源状态变更为[启用]
#
#   @自动化测试  @数据连接
#  Scenario Outline: 用例64.验证数据连接页面-数据源重新隐私发现能否成功
#    Given 已经存在数据连接<connect_name>，不存在则使用<db_source>,<ip>,<port>,<username>,<password>,<db_name>,<find_schema>新建
#    And 该连接隐私识别状态为[完成]
#    When 点击"更多-重新隐私发现"
#    Then 提示：需要对<connect_name>进行重新隐私发现吗
#    When 点击"全量发现"
#    Then 触发隐私发现成功
#    And <connect_name>隐私识别状态变为运行
#    And "重新隐私发现"按钮置灰不可点击
#    And 连接<connect_name>隐私识别状态为完成
#    When 回到数据连接列表页面
#    Then 搜索、删除对应数据连接<connect_name>成功
#    Examples:
#      | db_source  |  connect_name       | ip            | port  | db_name | username     | password | find_schema |
#      | Mysql      |  SHEN-Mysql-c1      | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#      | Postgresql |  SHEN-Postgresql-c1 | 192.168.7.240 | 5432  | testdb  | testor   | 123456   | autotest1   |
#      | IBM Db2    |  SHEN-DB2-c1        | 192.168.7.248 | 50000 | testdb  | db2inst1 | 123456   | autotest1   |
#      | Hive       |  SHEN-Hive-c1       | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#      | Presto     |  SHEN-Presto-c1     | 192.168.7.240 | 8080  | hive    | hive     | NULL     | autotest1   |
#      | ClickHouse |  SHEN-ClickHouse-c1 | 192.168.7.244 | 8123  | NULL    | NULL     | NULL     | PRIVATEDB   |
#      | Oracle     |  SHEN-Oracle-c1     | 192.168.7.240 | 1521  | ORCL    | TESTOR   | 123456   | autotest1   |
#      | Gbase      |  SHEN-Gbase-c1      | 192.168.7.244 | 5258  | gbase   | root     | root     | autotest1   |
#
#
#
#   @自动化测试  @数据连接
#  Scenario: 用例65.验证数据连接页面-数据源终止隐私发现能否成功
#    Given 页面存在发现全部数据源的数据连接B,不存在则新建
#      | db_source  |  conn_name     | ip            | port  | db_name | username     | password |
#      | Hive       |  SHEN-Hive-f1  | 192.168.7.242 | 10000 | default | hdfs     | 123456   |
#    And 该连接的隐私识别状态为[运行]
#    When 鼠标移入"更多"选项下
#    And 点击"终止隐私发现"
#    Then 弹框提示:"已终止隐私发现"
#    And 数据连接[SHEN-Hive-f1]隐私识别状态变为[终止]
#    When 鼠标悬浮移入隐私识别状态"终止"的字段上
#    Then 展示终止原因包含字段"任务手动终止"
#
#
# @自动化测试  @数据连接
#  Scenario: 用例66.验证新建hive-源端连接是否成功
#    Given 存在发现部分数据源的数据连接C,不存在则新建
#      | connect_type | target | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
#      |   数据库      |  源端 | Hive       |  new_hive_source  | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new_hive_source]存在
#    Then 删除数据连接[new_hive_source]成功
#
#
#  @自动化测试  @数据连接
#  Scenario: 用例67.验证新建hive-目标端连接是否成功
#    Given 使用下方参数，创建hive目标端数据连接
#     | connect_type | target | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema | save_type | url_path  | file_path | hive_user | hive_passwd |
#     |  数据库       | 目标端  | Hive       |  new_hive_target | 192.168.9.112 | 10000 | default | hdfs     | 123456   | autotest1   |   HDFS   | hdfs://IP:8020| /user/testor/ |   hdfs    |   hdfs   |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new_hive_target]存在
#    Then 删除数据连接[new_hive_target]成功
#
##
#  @自动化测试  @数据连接
#  Scenario: 用例68.验证新建hive-目标端-对象存储-连接是否成功
#    Given 使用下方参数，创建hive目标端数据连接
#      | connect_type | target| db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema | save_type | url_path  | file_path | hive_user | hive_passwd |
#      |   数据库      |  源端 | Hive       |  new_hive_target1 | 192.168.9.112 | 10000 | default | hdfs     | 123456   | autotest1   |   对象存储   | hdfs://IP:8020| /user/testor/ |   hdfs    |   hdfs   |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new_hive_target1]存在
#    Then 删除数据连接[new_hive_target1]成功
#
#   @自动化测试  @数据连接
#  Scenario: 用例69.验证新建mysql-目标端-连接是否成功
#    Given 使用下方参数，创建mysql目标端数据连接
#      | connect_type | target | db_source  |  conn_name       | ip            | port  | db_name | username     | password | find_schema |
#      |   数据库      |  源端  | Mysql      |  new-mysql-target1  | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new-mysql-target1]存在
#    Then 删除数据连接[new-mysql-target1]成功
#
###
###
#  @自动化测试  @数据连接
#  Scenario: 用例70.验证新建文件-源端-FTP连接是否成功
#    Given 使用下方参数，创建文件-源端-FTP数据连接
#     |connect_type |file_connect_type|  conn_name        | target | ip            | port | file_path   | username     | password | file_type | file_code |
#     |文件          |FTP              |  new_file_src     | 源端  | 192.168.7.240   | 21   | /home/home/ftpuser/csv/    | ftpuser     | datatunnel@kingsing   | null   |    null        |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new_file_src]存在
#    Then 删除数据连接[new_file_src]成功
###
###
#    @自动化测试  @数据连接
#  Scenario: 用例71.验证新建文件-目标端连接是否成功
#    Given 使用下方参数，创建文件-源端-FTP数据连接
#     |connect_type |file_connect_type|  conn_name        | target | ip            | port | file_path   | username     | password | file_type | file_code |
#     |文件          |FTP              |  new_file_des     | 目标端  | 192.168.7.248   | 21   | /home/ftpuser/csv/   | ftpuser     | datatunnel@kingsing   | null   |    null        |
#    When 进入数据连接列表页
#    Then 搜索和查询数据连接[new_file_des]存在
#    Then 删除数据连接[new_file_des]成功
###########################--待补充--############################
###################################--后续完成--############################
#
#
#
###  @自动化测试  @数据连接
###  Scenario: 用例72.验证新建API-连接是否成功
###    Given 使用下方参数，创建API数据连接
###      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
###      | Hive       |  new_hive_target | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
###    When 进入数据连接列表页
###    Then 搜索和查询数据连接[new_hive_target]存在
###    Then 删除数据连接[new_hive_target]成功
##
##
####  @自动化测试  @数据连接
###  Scenario: 用例73.验证新建消息队列-连接是否成功
###    Given 使用下方参数，创建消息队列-数据连接
###      | db_source  |  conn_name     | ip            | port  | db_name | username     | password | find_schema |
###      | Hive       |  new_hive_target | 192.168.7.242 | 10000 | default | hdfs     | 123456   | autotest1   |
###    When 进入数据连接列表页
###    Then 搜索和查询数据连接[new_hive_target]存在
###    Then 删除数据连接[new_hive_target]成功
#
#
##
#   @自动化测试  @数据连接 @后置
#  Scenario Outline: 用例74.后置处理：清空测试数据--指定数据
#    Given 已成功进入数据连接页面
#    When 数据连接名称<connect_name>非空
#    Then 数据连接名称<connect_name>非空时，删除连接成功
#    Examples:
#      | connect_name  |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | null   |
#      | abc   |
#      | abc   |
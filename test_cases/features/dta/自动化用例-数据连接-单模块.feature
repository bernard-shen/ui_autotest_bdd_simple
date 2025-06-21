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

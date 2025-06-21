Feature: <风险分析-自动化用例转化>

  ###1、因风险分析涉及执行sql语句；该用例集-依赖一条可用的数据源 和 脱敏任务；
  ###2、测试用例中-时间不固定不确定的，不做校验
  ###3、用例39、40-访问分组-开启用户认证，需确保后台有对应的可认证用shenpengfei1--相关用例中的用户数据
  ###4、风险分析单模块采用mysql：192.168.7.241数据源 和 对应脱敏任务；需确保数据源和代理任务本身无问题，可以正常连接访问；
  ###5、并发时，同时连接多条sql数据源，可能会造成数据库连接中断；时间充足的话，建议非并发执行；

  Background:
    Given 用户已登录数据访问网关平台1
    And 页面跳转至风险分析页面

  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例1-验证全局信息页面布局是否正确
    Given 已进入风险分析-全局信息页面
    When 查看所有页签时
    Then 从左到右依次展示："全局信息"、"访问用户"、"数据源"、"＋新增"
    When 查看搜索条件时
    Then 从左到右依次展示："会话状态"、"任务名称"、"风险等级"、"执行结果"
    And 搜索条件上部依次展示："更多搜索"链接、"重置"按钮、"查询"按钮
    When 查看列表信息时
    Then 从左到右依次展示："任务名称"、"数据源"、"会话编号"、"会话状态"、"SQL编号"、"SQL语句"、"访问用户IP"、"访问时间"、"执行结果"、"风险等级"、"安全操作"、"脱敏操作"


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例2-验证全局信息"更多搜索"是否可点击
    Given 已进入风险分析-全局信息页面
    When 点击"更多搜索"
    Then 弹出多选页面
    When 点击更多搜索-"全选"
    Then 所有选项均被勾选成功
#
  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例3-验证全局信息"更多搜索"弹出框是否可勾选单个或多个
    Given 已进入风险分析-全局信息页面
    When 点击"更多搜索"
    Then 弹出多选页面
    When 搜索选项勾选[访问分组]时
    Then 查询项增加字段[访问分组]
    When 搜索选项勾选[访问用户IP,个人用户,数据库用户]时
    Then 查询项增加字段[访问用户IP,个人用户,数据库用户]


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例4-验证全局信息查询条件是否支持单选
    Given 已进入风险分析-全局信息页面
    When 风险分析搜索取消全选
    When 查询条件增加[会话状态]-内容选择[断开]
    And 点击风险分析查询按钮
    Then 列表展示会话状态为断开的记录信息


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例5-验证全局信息查询条件是否支持多选
    Given 已进入风险分析-全局信息页面
    When 风险分析搜索取消全选
    When 查询条件增加[风险等级]-内容选择[无]
    And 查询条件再次增加[执行结果]-内容选择[成功]
    And 点击风险分析查询按钮
    Then 列表展示风险低、执行成功的记录信息


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例6-验证全局信息查询条件重置功能是否正常
    Given 已进入风险分析-全局信息页面
    When 查询条件增加[数据源]-内容输入[only_test]
    And 点击风险分析查询"重置"按钮
    Then 数据源内容清除为空


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例7-验证全局信息列表右侧的"+"是否可点击
    Given 已进入风险分析-全局信息页面
    When 点击列表右侧的"+"
    Then 正常弹出多选框


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例8-验证全局信息列表右侧的"+"是否可单选或多选
    Given 已进入风险分析-全局信息页面
    When 点击列表右侧的"+"
    And 列新增勾选选项[审计操作]
    And 点击新增"确定"
    Then 列表最右侧新增列[审计操作]
    When 点击列表右侧的"+"
    And 列新增勾选选项[影响行数,SQL功能类型]
    And 点击新增"确定"
    Then 列表最右侧新增列[影响行数,SQL功能类型]
    When 点击列表右侧的"+"
    And 点击勾选"全选"
    Then 所有选项均被勾选


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例9-验证全局信息列表右侧的"+"是否可取消勾选
    Given 已进入风险分析-全局信息页面
    When 点击列表右侧的"+"
    And 列新增勾选选项[影响行数,SQL功能类型]
    And 点击新增"确定"
    Then 列表最右侧新增列[影响行数,SQL功能类型]
    When 点击列表右侧的"+"
    And 取消勾选[影响行数,SQL功能类型]
    And 点击新增"确定"
    Then 列表最右侧去掉两列[影响行数,SQL功能类型]


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例10-验证双击列表中的任意一行数据，是否可以弹出SQL语句详情
    Given 已进入风险分析-全局信息页面
    And 风险分析的全局页面-列表中存在数据
    When 双击列表第一行数据
    Then 可以弹出SQL语句详情页


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例11-验证全局信息列表中的数据源，是否可点击
    Given 已进入风险分析-全局信息页面
    And 风险分析的全局页面-列表中存在数据
    When 点击列表首行"数据源"对应链接时
    Then 可弹出数据源详情页


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例12-验证全局信息列表中的数据源，是否可点击
    Given 已进入风险分析-全局信息页面
    And 风险分析的全局页面-列表中存在数据
    When 点击首行"SQL编号"下的链接时
    Then 可以弹出SQL语句详情页


  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例13-验证全局信息-SQL功能类型查询是否正常
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
      | select * from autotest1.all_private_table1 limit 2,20; |
      | select * from autotest1.all_private_table1 limit 3,30; |
      | select * from autotest1.all_private_table1 limit 4,40; |
      | select * from autotest1.all_private_table1 limit 50,5; |
      | select * from autotest1.all_private_table1 limit 11,0; |
      | select * from autotest1.update_table1 ut  left join autotest1.update_table2 ut2 on ut.UUID = ut2.UUID ;  |
      | SELECT COUNT(UUID) FROM autotest1.update_table1 ut WHERE uuid > 1000; |
      | select max(UUID) as mas_id from autotest1.update_table1 ut; |
      | update autotest1.update_table1 set NAME = 'hehe' where UUID = 1167; |
      | delete from autotest1.update_table2; |
      | delete from autotest1.update_table2 where UUID < 10; |
      | drop table autotest1.update_table_now1; |
    And 已进入风险分析-全局信息页面
    When 增加搜索条件[SQL功能类型]
    And 清空已选SQL功能类型
    And 增加列表列[SQL功能类型]
    And 选择搜索条件[SQL功能类型]为[DDL]
    And 点击风险分析查询按钮
    Then 风险分析全局信息中将展示[SQL功能类型]为[DDL]的数据
    When 清空已选SQL功能类型
    And 选择搜索条件[SQL功能类型]为[DQL]
    And 点击风险分析查询按钮
    Then 风险分析全局信息中将展示[SQL功能类型]为[DQL]的数据
    When 清空已选SQL功能类型
    And 选择搜索条件[SQL功能类型]为[DML]
    And 点击风险分析查询按钮
    Then 风险分析全局信息中将展示[SQL功能类型]为[DML]的数据

#
  @自动化测试 @脱敏任务 @风险分析 @全局信息
  Scenario: 用例14-验证全局信息-页面分页器能否正常使用
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问--循环执行22次
      | sql_command |
      | select * from autotest1.all_private_table1; |
    And 已经等待5s
    And 已进入风险分析-全局信息页面
    When 查看全局信息页面的列表时
    Then 分页器默认展示第一页的列表数据
    And 向左的箭头置灰无法点击
    When 全局信息页面展示多页的列表数据
    And 全局信息页面列表翻到最后一页
    Then 向右的箭头置灰无法点击
    When 在分页器中输入页码[2]
    And 点击enter键
    Then 页面列表自动跳转到对应的页数
    When 在分页器中选择展示20条/页
    Then 列表每页展示小于等于20条数据
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例15-验证"访问用户"页存在SQL语句，SQL详情页显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then 弹出SQL详情页，从上到下依次显示："风险等级"、"执行者信息"、"访问对象信息"、"执行内容信息"、"操作执行结果"、"安全防护"、"平台处理结果"


  ####颜色在css文件中，暂不校验；
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例16-验证"访问用户"页存在SQL语句，SQL详情页"风险等级"显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-风险等级部分，包含风险信息，且风险等级有颜色标识，枚举值从左到右依次显示："高风险"、"中风险"、"低风险"、"无风险"
##
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例17-验证"访问用户"页存在SQL语句，SQL详情页"风险信息"显示内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页显示的风险信息为操作风险的具体描述信息或"-"


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例18-验证"访问用户"页存在SQL语句，SQL详情页"执行者信息"显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then 执行者信息部分，依次从左到右显示："访问分组"、"访问用户IP"、"数据库用户"、"个人用户"、"客户端工具"、"访问时间"


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例19-验证"访问用户"页存在SQL语句，SQL详情页"执行者信息"显示内容是否正确
    Given 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页显示的执行者信息[访问分组]内容非空
    Then SQL详情页显示的执行者信息[访问用户IP]内容非空
    Then SQL详情页显示的执行者信息[数据库用户]内容非空
    Then SQL详情页显示的执行者信息[个人用户]内容非空
    Then SQL详情页显示的执行者信息[客户端工具]内容非空
    Then SQL详情页显示的执行者信息[访问时间]内容非空

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例20-验证"访问用户"页存在SQL语句，SQL详情页"访问对象信息"显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页访问对象信息部分，依次显示："数据库地址"、"数据库端口"、"影响对象"


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例21-验证"访问用户"页存在SQL语句，SQL详情页"访问对象信息"显示内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-访问对象信息[数据库地址]内容非空
    And SQL详情页-访问对象信息[数据库端口]内容非空
    And SQL详情页-访问对象信息[影响对象]内容非空

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例22-验证"访问用户"页存在SQL语句，SQL详情页"执行内容信息"显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-[执行内容信息]部分，字段依次显示：[SQL功能类型,操作类型,SQL编号,SQL语句]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例23-验证"访问用户"页存在SQL语句，SQL详情页"执行内容信息"显示内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-[执行内容信息]部分， 字段内容非空
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例24-验证"访问用户"页存在SQL语句，SQL详情页显示"操作执行结果"名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-[操作执行结果]部分，字段依次显示：[总耗时(ms),响应耗时(ms),请求时间,响应时间,脱敏耗时,执行结果,结果描述,错误代码,影响行数]

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例25-验证"访问用户"页存在SQL语句，SQL详情页"操作执行结果"显示内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-[操作执行结果]部分， 字段内容非空


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例26-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"显示名称和位置是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页-[安全防护]部分，字段依次显示：[SQL操作,命中规则,规则风险,安全操作,脱敏操作,脱敏方案]
    And SQL详情页-[安全防护]显示："SQL操作"、"安全操作"、"脱敏操作"


#
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例27-验证"访问用户"页存在SQL语句，SQL详情页"平台处理结果"显示内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 访问用户IP页存在SQL语句
    When 点击会话编号文本框下部的首行SQL语句时
    Then SQL详情页的[平台处理结果]内容显示"处理结果"为"成功"或"失败"
    ##需要指明如何操作才会失败
    ##And 如果失败会同时展示"失败原因"


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例28-【风险分析】验证"访问用户"页签的用户数统计是否正确
    Given 页面跳转至风险分析页面
    When 点击"访问用户"页签时
    Then 标签页名称变为[访问用户(1)]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例29-【风险分析】验证访问用户页的查询条件和按钮的名称和位置是否正确
    Given 已进入风险分析-访问用户页面
    Then 查询条件依次包含文本框:"访问IP:"、"时间范围"
    And 按钮名称显示："重置"、"查询"
    And 访问IP-默认提示文本：[输入访问IP]

### 时间不固定，不做校验
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例30-【风险分析】验证访问用户页的单个查询功能是否正常
    Given 已进入风险分析-访问用户页面
    When 访问IP输入为[192.168.7.100]
    And 点击"访问用户"页面的"查询"按钮
    Then 可以查询出访问IP为[192.168.7.100]的用户信息
#    Given 用户访问时间"2022-08-21 16:00:00"
#    When 开始时间和结束时间为"2022-08-21 00:00:00"到"2022-08-22 16:00:00"
#    And 点击"访问用户"页面的"查询"按钮后
#    Then 该用户内容仍旧可以展示查看


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario Outline: 用例31-【风险分析】验证访问用户IP页的组合查询功能是否正常
    Given 已进入风险分析-访问用户页面
    When 选择多个查询条件<access_ip>、<start_time>、<end_time>
    And 点击用户ip页面-风险分析"查询"按钮
    Then 可以查询出该条件下的<result>数据
    Examples:
      | access_ip     | start_time          | end_time            | result |
      | 192.168.7.100 | 2022-09-21 00:00:00 | 2024-09-22 16:00:00 | 192.168.7.100 |


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例32-【风险分析】验证访问用户IP页的重置按钮功能是否正常
    Given 已进入风险分析-访问用户页面
    When "访问IP"输入为[192.168.7.100]
    When 点击"访问用户"页面的"重置"按钮
    Then 查询条件ip内容清空

#### 用例删除，目前已支持模糊查询
####  @自动化测试 @脱敏任务 @风险分析 @访问用户
####  Scenario: 用例33-【风险分析】验证访问用户IP页的"访问用户IP"不支持模糊查询
####    Given 已进入风险分析-访问用户页面
####    And 当前页面首行ip地址为A
####    When 输入"访问IP"A的前半部分
####    And 点击"访问用户"页面的"查询"按钮
####    Then 系统不支持模糊查询，无法查询出结果


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例34-【风险分析】验证访问用户IP页左侧的"访问IP"可折叠
    Given 已进入风险分析-访问用户页面
    When 展开首个卡片
    Then 卡片展开成功
    When 收起首个卡片
    Then 卡片收起成功


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例35-【风险分析】验证访问用户IP页左侧内容是否最新数据源
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
    And 已经等待5s
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新的用户ip
    Then 页面左侧最上方显示最新访问的一个数据源[SHEN-mysql666]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例36-【风险分析】验证访问用户IP页左侧的访问IP数据源不变但时间改变，是否显示最新的数据源
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
    And 再次进入风险分析-访问用户页面
    When 点击访问用户-最新的用户ip
    Then 页面左侧最上方显示访问的数据源为[SHEN-mysql666]，访问时间为time1
    Given 已经等待5s
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
    When 再次进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    Then 页面左侧最上方显示最新访问的一个数据源[SHEN-mysql666]
    And 访问时间time2大于time1


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例37-【风险分析】验证访问用户IP页左侧内容，时间是否倒序排列
    Given 已进入风险分析-访问用户页面
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    And 已经等待5s
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    And 已进入风险分析-访问用户页面
    When 展开首个卡片
    Then 访问时间倒序排列
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例38-【风险分析】验证访问用户IP页的信息是否悬浮显示
    Given 已进入风险分析-访问用户页面
    When 鼠标悬浮在访问用户IP时
    Then 显示访问用户IP的访问分组信息:"访问分组"、"分组类别"、"客户端工具"、"数据库用户"
##
##
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例39-【风险分析】验证访问用户IP页的IP地址悬浮显示-访问分组和分组类别正确
    Given 已进入风险分析-访问用户页面
    When 鼠标悬浮在访问用户IP时
    Then 如果存在多个分组,多列用"|"分隔
    And 和该IP对应的访问分组和分组类别正确


  ##### 要用开认证的分组，执行login认证，才算用户访问过
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例40-【风险分析】验证访问用户IP页的"显示用户"是否可点击
    Given 已进入风险分析-访问用户页面
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | login -ushenpengfei1 -p!Qaz2wsx; |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    When 再次进入风险分析-访问用户页面
    And 点击用户IP右侧的"显示用户"时
    Then "显示用户"切换为"不显示用户"
    When 点击用户IP右侧的"不显示用户"时
    Then "不显示用户"切换为"显示用户"


################################################################################
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例41-【风险分析】验证访问用户IP页的"显示用户"是否可点击，并展示所有数据源
    Given 已进入风险分析-访问用户页面
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
      | Mysql      | SHEN-mysql888   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
      | SHEN_mysql_DD | 访问防护    | SHEN-mysql888 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    And 脱敏任务[SHEN_mysql_DD]的代理端口为B
    And 脱敏任务[SHEN_mysql_DD]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    When 再次进入风险分析-访问用户页面
    And 点击用户IP右侧的"显示用户"
    And 点击访问用户ip左侧下拉
    And 点击用户[shenpengfei1]左侧的展开按钮
    Then 下方用户[shenpengfei1]访问过的数据源包含:[SHEN-mysql777]和[SHEN-mysql888]

#
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例42-【风险分析】验证访问用户IP页"所有会话"按钮右侧-帮助图标文案内容是否正确
    Given 已进入风险分析-访问用户页面
    When 可以看到右侧的按钮："所有会话"
    And 查看按钮右侧的问号图标
    Then 显示文本内容：[点击所有会话，可查看此数据源中所有操作]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例43-【风险分析】验证访问用户IP页"所有会话"是否显示所有会话的信息
    Given 已进入风险分析-访问用户页面
    When 展开访问用户ip，点击第一条数据源
    Then 此时右侧数据SQL操作条数，成功条数，失败条数，高风险条数，脱敏操作条数分别为a,b,c,d,e
    When 点击"所有会话"
    Then 此时右侧SQL操作条数，成功条数，失败条数，高风险条数，脱敏操作条数分别为A,B,C,D,E
    And 数据a,b,c,d,e小于等于对应的A,B,C,D,E
##
#
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例44-【风险分析】验证访问用户IP页会话语句，是否可点击并弹出SQL详情页
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
    And 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    When 点击会话编号下面展开的SQL语句时
    Then 语句可点击并正常弹出SQL详情
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例45-【风险分析】验证访问用户IP页的"持续时间"显示是否正常
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task2 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task2]的代理端口为B
    And 脱敏任务[SHEN_mysql_task2]已正常启动
    And 存在脱敏任务代理端连接D，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    And 已经等待5s
    And 运行中的脱敏任务[SHEN_mysql_task2]终止后再次重新启动
    And 已进入风险分析-访问用户页面
    When 选择第一个用户IP下的数据源[SHEN-mysql666]
    Then 对应的持续时间显示该数据源被访问的开始时间和结束时间的区间


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例46-【风险分析】验证访问用户IP页的"会话编号"左侧展开收起正常
    Given 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    When 点击右侧"会话编号"左侧的收起按钮
    Then sql语句展开收起正常
    When 点击右侧"会话编号"左侧的展开按钮
    Then sql语句展开展开正常
#
#
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例47-【风险分析】验证访问用户IP页的右侧下方查询条件字段显示、默认文本内容是否正确
    Given 已进入风险分析-访问用户页面
    Then 界面右侧下方的查询条件从左到右依次显示下拉框："会话编号"、"会话状态"
    And 默认提示文本内容：[请选择]
#
#
  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例48-【风险分析】验证访问用户IP页的"会话状态"下拉框显示的枚举值是否正确
    Given 已进入风险分析-访问用户页面
    When 点击"会话状态"下拉选项
    Then 可以看到枚举值从上到下分别显示"请求连接"、"连接中"、"断开"


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例49-【风险分析】验证访问用户IP页的"会话状态"下拉选择"请求连接"，是否可正常筛选出结果
    Given 已进入风险分析-访问用户页面
    When 点击"会话状态"下拉选项
    And 选择其中一个选项"断开"
    Then 筛选出的结果全部为断开连接状态的SQL语句


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例50-【风险分析】验证访问用户IP页的"会话状态"下拉选择"连接中"，是否可正常筛选出结果
    Given 已进入风险分析-访问用户页面
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接C，并执行以下sql访问, 保持连接状态
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    When 再次进入风险分析-访问用户页面
    And 右侧会话状态选择为"连接中"
    Then 筛选出的结果全部为连接中状态的SQL语句
    And 访问连接断开连接成功


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例51-【风险分析】访问用户IP页的右侧下方鼠标悬浮在每条SQL操作语句时，执行信息内容是否正确
    Given 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    When 鼠标悬浮在第一条SQL操作语句时
    Then 显示此条sql的执行信息内容正确,包括"执行结果"、"风险等级"、"安全操作"、"脱敏操作"
    And 执行结果的枚举值包含：成功、失败
    And 风险等级的枚举值包含：无风险、低风险、中风险、高风险、致命风险
    And 安全操作的枚举值包含：允许、放行、拦截、阻断、脱敏配置
    And 脱敏操作的枚举值包含：是、否
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例52-【风险分析】验证访问用户IP页的每个SQL语句右侧，执行耗时展示
    Given 已进入风险分析-访问用户页面
    When 点击访问用户-最新用户ip-首条数据源
    When 查看一个SQL语句右侧对应的耗时
    Then 每个SQL语句右侧都显示"耗时(s)"，间隔0.005s


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例53-【风险分析】验证访问用户IP页的会话是否按操作时间进行倒序排列
    Given 已进入风险分析-访问用户页面
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接C，并执行以下sql访问, 单条sql执行后，停留5s;
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    When 再次进入风险分析-访问用户页面
    And 点击脱敏任务-对应的数据源[SHEN-mysql666]
    And 点击查看数据源对应的最新两次sql语句的访问时间
    Then 会话内的SQL语句按照执行的时间进行倒序排序
#

  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例54-【风险分析】访问用户IP页的持续时间显示数据是否正确-有正在进行的操作
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql999   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_EE | 访问防护    | SHEN-mysql999 | 2010      | auto-非认证分组1      | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_EE]的代理端口为B
    And 脱敏任务[SHEN_mysql_EE]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问，保持连接状态
      | sql_command |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table2 apt; |
    And 已进入风险分析-访问用户页面
    When 风险分析选择数据源[SHEN-mysql999]
    And 查看"持续时间"数据时
    Then 显示的是："开始时间-"
    And 访问连接断开连接成功


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例55-【风险分析】访问用户IP页的左侧显示内容，是否是查询条件"访问IP"、"时间范围"筛选后的结果
    Given 已进入风险分析-访问用户页面
    When "时间范围"输入数据为今天到明天
    And 点击风险分析-访问用户-查询按钮
    Then 页面左侧展示数据源"时间范围"在今天


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例56-验证数据源页面的页面布局是否正常
    Given 已经进入到风险分析-数据源页签
    Then 左侧板块显示系统存在数据源
    And 数据源上方显示筛选条件："数据源名称"
    And 右侧上部板块显示默认查询条件"显示频率"、"时间范围"
    ### canvas标签为js绘制的位图，暂无法定位位图内的内容
    ###And 右侧上部板块显示"无风险"、"低风险"、"中风险"、"高风险"
    ###And "显示频率"下方横坐标默认显示日期，纵坐标默认显示"0"、"1"、"2"、"3"、"4"
    And 右侧中部显示查询条件为"会话状态"、"安全操作"、"风险等级"、"执行结果"，按钮依次显示："重置"、"查询"
    And 右侧中部显示列表字段为"访问用户IP","任务名称","会话编号","会话状态","SQL编号","SQL语句","风险等级","执行结果","安全操作"
    And 板块2页面最下方左侧置灰显示为"双击单条数据可查看SQL语句详情"，在右侧显示为分页器包含"共 页","前往1页"
#

  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例57-验证点击数据源页签后，是否正确显示数据源个数
    Given 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    Then 数据源页签显示:"数据源(3)"

#
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例58-验证数据源页面，查询条件"数据源名称"是否可下拉选择
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    And 下拉点击查询条件中的"数据源名称"
    Then 下拉选择列表可以看到[SHEN-mysql777]
#
#
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例59-验证数据源页面，查询条件"数据源名称"下拉选择后的筛选结果是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    And 数据源名称下拉选择[SHEN-mysql777]
    Then 左侧数据源仅可以看到[SHEN-mysql777]


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例60-验证数据源页面，"数据源名称"右侧的数据源是否可点击弹出数据源详情
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    And 数据源名称下拉选择[SHEN-mysql777]
    And 点击首个数据源的"数据源名称"时
    Then 弹出数据源详情


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例61-验证数据源页面，数据源卡片内显示字段是否正确
    Given 已经进入到风险分析-数据源页签
    Then 数据源名称下部左侧显示字段:"SQL语句(条)"、"风险语句(条）"、"访问用户IP(个)"
    And 右侧显示每个字段对应的"当前/全部"对应的数值


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例62-验证数据源页面，每个数据源卡片内的"访问用户IP(个)"是否可展开
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    And 数据源名称下拉选择[SHEN-mysql777]
    And 展开数据源卡片内的"访问用户IP(个)"
    Then 可以看到对应的访问ip地址
    When 鼠标点击ip左侧的展开按钮
    Then ip展开正常
#
#
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例63-验证数据源页面，每个数据源卡片内的"访问用户IP(个)"是否显示用户IP以及IP用户
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 数据源页面中存在多个数据源
    And 数据源名称下拉选择[SHEN-mysql777]
    When 展开数据源卡片内的"访问用户IP(个)"
    Then 可以看到对应的访问ip地址
    When 鼠标点击ip左侧的展开按钮
    Then ip展开正常
    And 正常展示访问ip的用户[shenpengfei1]

#
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例64-验证数据源页面，数据源卡片查询组件能否进行查询
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | login -ushenpengfei1 -p!Qaz2wsx |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
    And 已经进入到风险分析-数据源页签
    When 查看数据源卡片时
    And 数据源名称下拉选择[SHEN-mysql777]
    Then 左侧数据源仅可以看到[SHEN-mysql777]


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例65-验证数据源页面，查看风险分布页面显示频率下拉是否可选"分钟"、"小时"、"天"
    Given 已经进入到风险分析-数据源页签
    When 查看风险分布曲线部分
    And 点击显示频率下拉框
    Then 显示可下拉选择"分钟"、"小时"、"天"


  ##### 通道逻辑，drop table可能会命中不同的规则；
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例66-验证数据源页面,当存在执行失败SQL操作语句时，鼠标悬浮是否可查看失败原因
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql999   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_EE | 访问防护    | SHEN-mysql999 | 2010      | auto-非认证分组1      | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_EE]的代理端口为B
    And 脱敏任务[SHEN_mysql_EE]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | drop table autotest1.all_private_table1; |
    And 已经进入到风险分析-数据源页签
    When 数据源名称下拉选择[SHEN-mysql999]
    And 点击数据源"访问用户IP(个)"
    And 会话列表查询选择-执行结果为[失败]的会话
    And 操作鼠标放置首行"执行结果"为"失败"的图标"!"上时
    Then 悬浮显示具体失败的原因[禁止 drop table 操作|禁止 drop语句]


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例67-验证数据源页面列表下方提示信息是否展示正确
    Given 已经进入到风险分析-数据源页签
    Then 访问数据列表下方提示信息展示：[提示：双击单条数据可查看SQL语句详情]


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例68-验证数据源页面,列表下方双击单条数据是否可查看SQL语句详情
    Given 已经进入到风险分析-数据源页签
    And 系统中已存在多行"访问用户IP"对应列表数据
    When 双击首行"访问用户IP"对应数据时
    Then 页面右侧弹出SQL语句详情页面
#

  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例69-验证数据源页面,SQL语句详情页面显示是否正常
    Given 已经进入到风险分析-数据源页签
    And 系统中已存在多行"访问用户IP"对应列表数据
    When 点击首行"SQL编号"时
    Then 页面右侧弹出SQL语句详情页面
#

###################################################################
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例70-验证数据源页面会话状态下拉枚举值是否正确
    Given 已经进入到风险分析-数据源页签
    When 下拉查看列表查询条件中的"会话状态"
    Then 枚举值依次显示:"请求连接"、"连接中"、"断开"


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例71-验证数据源页面安全操作下拉枚举值是否正确
    Given 已经进入到风险分析-数据源页签
    When 查看下方会话列表部分
    And 下拉查看查询条件中的"安全操作"
    Then 枚举值依次显示:"拦截"、"终止"、"放行"


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例72-验证数据源页面风险等级下拉枚举值是否正确
    Given 已经进入到风险分析-数据源页签
    When 查看下方会话列表部分
    And 下拉查看查询条件中的"风险等级"
    Then 枚举值依次显示:"无"、"低"、"中"、"高"
#
#
  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例73-验证数据源页面执行结果下拉枚举值是否正确
    Given 已经进入到风险分析-数据源页签
    When 查看下方会话列表部分
    When 下拉查看查询条件中的"执行结果"
    Then 枚举值依次显示:"失败"、"成功"


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario Outline: 用例74-验证数据源页面，组合查询是否成功
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
      | select * from autotest1.all_private_table1 limit 2,20; |
      | select * from autotest1.all_private_table1 limit 3,30; |
      | select * from autotest1.all_private_table1 limit 4,40; |
      | select * from autotest1.all_private_table1 limit 50,5; |
      | select * from autotest1.all_private_table1 limit 11,0; |
      | select * from autotest1.update_table1 ut  left join autotest1.update_table2 ut2 on ut.UUID = ut2.UUID ;  |
      | SELECT COUNT(UUID) FROM autotest1.update_table1 ut WHERE uuid > 1000; |
      | select max(UUID) as mas_id from autotest1.update_table1 ut; |
      | update autotest1.update_table1 set NAME = 'hehe' where UUID = 1167; |
      | delete from autotest1.update_table2; |
      | delete from autotest1.update_table2 where UUID < 10; |
      | drop table autotest1.update_table_now1; |
    And 已经进入到风险分析-数据源页签
    When 查看下方会话列表部分
    When 依次下拉选择"会话状态"<dialogue_state>，"安全操作"<safety_operation>，"风险等级"<risk_level>，"执行结果"<execution_result>
    And 点击风险分析-数据源页-列表"查询"
    Then 页面应该显示符合查询条件的数据
    Examples:
      | dialogue_state | safety_operation | risk_level | execution_result |
      | 断开            |  拦截             |  中        | 失败              |
      | 断开            |  放行             |  无        | 成功              |
#

  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario Outline: 用例75-验证数据源页面，单个查询是否成功
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | create table autotest1.update_table_now1 (select * from autotest1.all_private_table1 apt ); |
      | select * from autotest1.all_private_table1; |
      | select * from autotest1.all_private_table1 apt; |
      | select NAME from autotest1.all_private_table1 apt limit 20; |
      | select * from autotest1.all_private_table1 limit 0,10; |
      | select * from autotest1.all_private_table1 limit 1,10; |
      | select * from autotest1.all_private_table1 limit 2,20; |
      | select * from autotest1.all_private_table1 limit 3,30; |
      | select * from autotest1.all_private_table1 limit 4,40; |
      | select * from autotest1.all_private_table1 limit 50,5; |
      | select * from autotest1.all_private_table1 limit 11,0; |
      | select * from autotest1.update_table1 ut  left join autotest1.update_table2 ut2 on ut.UUID = ut2.UUID ;  |
      | SELECT COUNT(UUID) FROM autotest1.update_table1 ut WHERE uuid > 1000; |
      | select max(UUID) as mas_id from autotest1.update_table1 ut; |
      | update autotest1.update_table1 set NAME = 'hehe' where UUID = 1167; |
      | delete from autotest1.update_table2; |
      | delete from autotest1.update_table2 where UUID < 10; |
      | drop table autotest1.update_table_now1; |
    And 已经进入到风险分析-数据源页签
    When 依次下拉选择"会话状态"<dialogue_state>，"安全操作"<safety_operation>，"风险等级"<risk_level>，"执行结果"<execution_result>
    And 点击风险分析-数据源页-列表"查询"
    Then 页面应该显示符合查询条件的数据1
    Examples:
      | dialogue_state | safety_operation | risk_level | execution_result |
      | 断开            | null             |  null      | null             |
      | null           | 拦截              |  null      | null             |
      | null           |  null            | 中          | null             |
      | null           |  null            | null        | 成功              |


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例76-验证数据源页面，重置功能是否正常
    Given 已经进入到风险分析-数据源页签
    When 下拉选择"会话状态"-[断开]
    And 点击风险分析-数据源查询"重置"
    Then 会话状态查询条件清空


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例77-验证数据源页面，鼠标点击SQL语句详情页面外的区域时，是否可关闭SQL语句详情页面
    Given 已经进入到风险分析-数据源页签
    And 系统中已存在多行"访问用户IP"对应列表数据
    When 双击首行"访问用户IP"对应数据时
    Then 页面右侧弹出SQL语句详情页面
    When 操作鼠标点击SQL语句详情页面外的区域时
    Then SQL语句详情页面关闭，并返回至风险分析页面数据源页签


  @自动化测试 @脱敏任务 @风险分析 @数据源
  Scenario: 用例78-验证数据源页面，点击"X"是否可关闭SQL语句详情页面
    Given 已经进入到风险分析-数据源页签
    And 系统中已存在多行"访问用户IP"对应列表数据
    When 双击首行"访问用户IP"对应数据时
    Then 页面右侧弹出SQL语句详情页面
    When 点击SQL语句详情页右上角"X"时
    Then SQL语句详情页面关闭，并返回至风险分析页面数据源页签


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例79-验证自定义页签的"＋新增"，是否可点击并正常弹窗
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    Then 可以正常弹出自定义页签的新增窗口


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例80-验证自定义页签弹窗的页面元素是否正常展示
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    Then 新增窗口显示"新增"标题
    And 从上到下依次显示字段名称:"页签名称"、"页面显示"、"筛选条件"
    And 页面显示字段下拉枚举值包含:"全局信息"、"访问用户"、"数据源"
    And 包含两个按钮，从左到右依次显示:"取消"、"保存"


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例81-验证自定义页签"页面显示"默认显示的项是否正确
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 查看弹窗内容时
    Then "页面显示"默认显示的是[全局信息]


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario Outline: 用例82-验证自定义页签，"页面显示"选择"全局信息"，能否新增成功
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 新增窗口输入"页签名称"<tag_name>、"页面显示"<page_display>、筛选条件：访问分组<access_group>、SQL功能类型<sql_type>、脱敏操作<mask_operation>
    And 点击页签新增保存
    Then 页签新增成功，风险分析页签多了一个新增页签，名称和设置的名称<tag_name>保持一致
    When 点击自定义的页签<tag_name>名称后的"X"
    And 点击页签删除"确定"按钮
    Then 页签删除成功
    Examples:
      | tag_name | page_display | access_group | sql_type | mask_operation |
      | AUTO-全局自定义1 | 全局信息  |  auto-非认证分组1     | DDL  | 是             |
      | AUTO-全局自定义2 | 全局信息  | auto-认证分组1 | DQL  | 否             |


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario Outline: 用例83-验证自定义页签，"页面显示"选择"访问用户"，能否新增成功
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 新增窗口输入"页签名称"<tag_name>、"页面显示"<page_display>、选择访问时间-"开始时间"<start_time>、"结束时间"<end_time>、"访问用户IP"<user_ip>
    And 点击页签新增保存
    Then 页签新增成功，风险分析页签多了一个新增页签，名称和设置的名称<tag_name>保持一致
    When 点击自定义的页签<tag_name>名称后的"X"
    And 点击页签删除"确定"按钮
    Then 页签删除成功
    Examples:
      | tag_name | page_display  | start_time | end_time |user_ip |
      | AUTO-全局自定义3 | 访问用户 | 2022-09-23 00:00:00 | 2023-09-24 00:00:00 | 192.168.7.100 |
#

  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario Outline: 用例84-验证自定义页签，"页面显示"选择"数据源"，能否新增成功
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 新增窗口输入"页签名称"<tag_name>、"页面显示"<page_display>、"筛选条件:数据源"<data_source>、"筛选条件:访问用户IP"<user_ip>
    And 点击页签新增保存
    Then 页签新增成功，风险分析页签多了一个新增页签，名称和设置的名称<tag_name>保持一致
    When 点击自定义的页签<tag_name>名称后的"X"
    And 点击页签删除"确定"按钮
    Then 页签删除成功
    Examples:
      | tag_name | page_display | data_source |user_ip |
      | 数据源自定义1  | 数据源  | SHEN-mysql666 | 192.168.7.78 |
      | 数据源自定义2  | 数据源  | SHEN-mysql777 | 192.168.7.200 |


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例85-验证自定义页签，能否取消成功
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 新增窗口输入"页签名称"输入[auto测试1]、"页面显示"默认"全局信息"、"筛选条件"下拉选择"数据源"
    And 筛选条件数据源输入[mysql-test1]
    And 点击页签新增"取消按钮"
    Then 页签新增弹窗消失


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例86-验证自定义页签，能否删除成功
    Given 页面跳转至风险分析页面
    And 点击"新增"页签[auto-test001]并新增成功
    When 点击自定义页签[auto-test001]名称后的"X"
    And 点击页签删除"确定"按钮
    Then 页签删除成功

#
  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例87-验证自定义页签，删除提示信息是否正确
    Given 页面跳转至风险分析页面
    And 点击"新增"页签[auto-test002]并新增成功
    When 点击自定义页签[auto-test002]名称后的"X"
    Then 弹出提示窗口：[删除此页签后将不恢复，确定要删除吗？]
    When 点击页签删除"确定"按钮
    Then 页签删除提示:[页签删除成功]

#
  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例88-验证自定义页签，筛选条件选择后能否删除成功
    Given 页面跳转至风险分析页面
    When 点击"新增"页签
    And 筛选条件选择"数据源"
    Then 筛选条件下面增加一行必填项："数据源"
    When 点击筛选条件中数据源后面的"X"或筛选条件下的数据源文本框右侧的"X"
    Then "数据源"筛选条件被删除


  @自动化测试 @脱敏任务 @风险分析 @自定义页签
  Scenario: 用例89-验证自定义页签-新建成功的页签，每次进入是否为设置的筛选条件且数据展示正确
    Given 页面跳转至风险分析页面
    And 点击"新增"页签[auto-test003]并新增成功
    When 翻到其他页面再重新进入[auto-test003]页签时
    Then 左上方筛选条件仅展示[数据源]
    And 数据源内默认筛选值为[test111]
    When 点击自定义页签[auto-test003]名称后的"X"
    And 点击页签删除"确定"按钮
    Then 页签删除成功


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例90-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"显示内容是否正确
    Given 已进入风险分析-全局信息页面
    When 增加搜索条件[SQL语句]
    And 输入sql语句[drop table autotest1.update_table_now1]并查询
    And 双击列表第一行数据
    Then 可以弹出SQL语句详情页
    Then SQL详情页-安全防护,SQL操作内容为[DROP TABLE]
    Then SQL详情页-安全防护,[命中规则]内容为[禁止 drop语句]
    Then SQL详情页-安全防护,[规则风险]内容为[高风险]
    Then SQL详情页-安全防护,[安全操作]内容为[拦截]
    Then SQL详情页-安全防护,[脱敏操作]内容为[null]
    Then SQL详情页-安全防护,[脱敏方案]内容为[-]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例91-验证"访问用户"页存在SQL语句，SQL详情页的字段内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
    And 已进入风险分析-全局信息页面
    When 增加搜索条件[SQL语句]
    And 输入sql语句[select * from autotest1.all_private_table1]并查询
    When 双击列表第一行数据
    Then 可以弹出SQL语句详情页
    Then SQL详情页-安全防护-首行数据展示-字段名称[uid]，脱敏方式[未脱敏]，数据集[7972426]
    And SQL详情页-安全防护-第二行数据展示-字段名称[name]，脱敏方式[高仿真脱敏]，数据集[[植渤]]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例92-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"字段下方的"查看更多"是否可点击并弹窗
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1; |
    And 已进入风险分析-全局信息页面
    When 增加搜索条件[SQL语句]
    And 输入sql语句[select * from autotest1.all_private_table1]并查询
    When 双击列表第一行数据
    Then 可以弹出SQL语句详情页
    When 点击SQL详情页-安全防护-下方"查看更多"按钮
    Then 正常弹出"脱敏数据详情"页
    And 分页每页默认10行


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例93-验证"访问用户"页存在SQL语句，SQL详情页"安全防护"字段下方的"查看更多"显示字段内容是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问
      | sql_command |
      | select * from autotest1.all_private_table1 limit 100; |
    And 已进入风险分析-全局信息页面
    When 增加搜索条件[SQL语句]
    And 输入sql语句[select * from autotest1.all_private_table1 limit 100]并查询
    When 双击列表第一行数据
    Then 可以弹出SQL语句详情页
    When 点击SQL详情页-安全防护-下方"查看更多"按钮
    Then 正常弹出"脱敏数据详情"页
    And 详情页字段名包括[字段名称,脱敏方式,数据集]
    And 第三个字段包含内容：[phone_number,高仿真脱敏,[14514366561],[13244305889],[14718277262]]
    And 第四个字段包含内容：[id_no,高仿真脱敏,[231024196402253572],[420505198308247848],[41062119610701601X]]


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例94-【风险分析】验证访问用户IP页从其他界面切入，SQL操作小于20条时，默认展示是否正确一致
    Given 已进入风险分析-访问用户页面
    When 展开访问用户ip，点击第一条数据源
    Then SQL操作条数 和 会话下方sql语句条数 一致


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例95-【风险分析】验证访问用户IP页从其他界面切入，SQL操作大于20条时，默认展示是否正确
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql666   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_task1 | 访问防护    | SHEN-mysql666 | 2010      | auto-非认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_task1]的代理端口为B
    And 脱敏任务[SHEN_mysql_task1]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问--循环执行22次
      | sql_command |
      | select * from autotest1.all_private_table1 limit 16; |
    When 再次进入风险分析-访问用户页面
    When 选择第一个用户IP下的数据源[SHEN-mysql666]
    Then 右侧SQL操作大于[20]条
    And 会话下方sql语句只展示20条


  @自动化测试 @脱敏任务 @风险分析 @访问用户
  Scenario: 用例96-【风险分析】验证访问用户IP页从其他界面切入且SQL操作大于40条，点击查看更多按钮展示是否正常
    Given 已经存在mysql数据连接B,不存在则新建
      | db_source  | conn_name       | ip            | port  | db_name | username     | password | find_schema |
      | Mysql      | SHEN-mysql777   | 192.168.7.241 | 3306  | testor  | root     | 123456   | autotest1   |
    And 存在访问分组[auto-认证分组1]，且分组已开启身份认证
    And 存在下方脱敏任务B，不存在则新建
      | task_name        | task_type | conn_name      | proxy_port | access_group | masking_plan  | safety_plan |
      | SHEN_mysql_CC | 访问防护    | SHEN-mysql777 | 2010      | auto-认证分组1       | 默认脱敏方案   | 默认安全方案  |
    And 脱敏任务[SHEN_mysql_CC]的代理端口为B
    And 脱敏任务[SHEN_mysql_CC]已正常启动
    And 存在脱敏任务代理端连接B，并执行以下sql访问--循环执行42次
      | sql_command |
      | select * from autotest1.all_private_table1; |
    When 再次进入风险分析-访问用户页面
    When 展开访问用户ip，点击第一条数据源
    Then 右侧SQL操作大于[40]条
    When 点击sql列表下方按钮查看更多时
    Then 会话下方sql语句多展示20条，即共展示40条数据
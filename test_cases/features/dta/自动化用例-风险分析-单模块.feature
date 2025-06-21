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

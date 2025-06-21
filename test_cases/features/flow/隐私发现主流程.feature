Feature: 隐私发现主流程测试

  @流程测试-隐私发现主流程
  Scenario: 用例1:-隐私发现主流程-测试001
    Given 创建数据连接[data_connect]
    Given 触发隐私发现[exe_secret_find_task]
    Given 查看隐私发现结果[check_result]

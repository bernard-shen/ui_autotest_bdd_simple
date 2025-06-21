
# AutomationTest
# 该框架为2022年搭建，主要使用playwright + 行为驱动pytest-bdd，别问为什么（公司已有海量的行为驱动用例，且老板要求能直接用这些用例）；
# 已删除关键业务线模块和大量用例，仅保留个别用例样例；当时技术水平有限，该框架仅供参考。
# [使用说明]()

## 1、下载需要的软件清单：

    git、python、pycharm、allure、playwright

## 2、安装。--以下安装可能需要管理员密码；

    2.1、python安装时记得勾选添加环境变量；
    2.2、allure解压到项目文件夹下，管理员身份运行allure.bat（windows环境）添加环境变量；


## 3、确认代码仓库权限：
    点进项目复制克隆链接：

## 4、在pycharm里git导入项目：

## 5、一般新项目会自动跳出添加虚拟环境，没有的话手动添加虚拟环境；

    设置pip源：
    pip仓库
    客户端配置
    单次下载
    以下载grpcio==1.24.3 为例
    pip3 install -i http://192.168.7.8:8081/repository/pip-proxy-group/simple --trusted-host 192.168.7.8 grpcio==1.24.3
    修改默认配置
    pip3 config set global.index-url http://192.168.7.8:8081/repository/pip-proxy-group/simple --trusted-host 192.168.7.8
    然后安装需要的插件库：pip install -r .\requirements.txt --trusted-host 192.168.7.8
    
    
    然后配置playwright环境：
    
    只需解压依赖至相应目录下
    
    Windows：%USERPROFILE%\AppData\Local
    MacOS：~/Library/Caches
    Linux：~/.cache

## 6、文件结构：
    
    test_cases-存放测试用例：feature文件 和 对应的py文件；====test_cases 和 pages 为自动化代码主要实现区域；
    base,common封装的公共类；config-配置文件；init初始化模块；pages-页面对象封装-PO; pojo对象结构；test_data-测试数据--目前简单数据直接放在feature里；
    

## 7、自动化-初步实现步骤：--仅当前公司

    筛选模块最新版本用例
    主流程用例筛选拆分(遵循语法、步骤细化)
    feature文件导入–可以在pycharm中用快捷键alt+enter；选择生成步骤代码；
    需要录制时，terminal控制台输入：playwright codegen  "此处为待测页面ip地址"，开启录制；
    录制步骤代码，并copy到对应的步骤代码函数下
    修改代码-确认定位唯一、操作正确、异常捕捉、加上正确的断言；
    跑.py文件，生产报告；
    手动生成报告：allure serve +报告生成路径
    自动生成报告：allure添加环境变量有问题-待更新；
    做其他相关优化；

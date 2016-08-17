# Auto Monkey For Android #

### 版本 1.1

### 功能简介 ###
1. 完全自动：只需要负责连接设备
2. 支持多个设备
3. 支持随时断开设备、插入新设备，每5s定时检测设备自动运行
4. 崩溃后，发送邮件，邮件内容：执行时长、crash log
5. 支持Windows、Mac系统
6. 支持配置文件

### 系统及环境、依赖 ###
1. 测试环境：Mac OS、Windows 10、Python 2.7.10
2. 配置 **adb**

### 配置修改 ###
user_config/default.conf

    ```
    [config]
    package_name = com.testerhome.nativeandroid
    adb_location = /Users/smzdm/Documents/01_Android/adt-bundle-mac-x86_64-20140702/sdk/platform-tools/adb

    # 设置邮箱服务器
    mail_host = smtp.xxxx.com
    # 邮箱账号
    mail_user = xxxxxx@xxx.com
    # 邮箱密码
    mail_pass = ******

    [mail_to_list]
    # 设置发送给收件人, 格式如下，等号右侧留空
    aaaaaa@163.com =
    bbbbbb@163.com =

    [monkey_parameters]
    # monkey 相关的参数，需要哪些，直接在下面按格式添加去掉前面的 # 符号即可. 不需要赋值的参数等号后面留空就可以
    -v =
    --throttle = 300
    --pct-trackball = 0
    --pct-syskeys = 5
    --pct-nav = 0
    --pct-anyevent = 0
    # --pct-majornav = 0
    # --pct-appswitch = 0
    # --pct-flip = 0
    # --pct-pinchzoom = 0
    # --pct-permission = 0
    # --pct-touch = 0
    # --pct-motion = 0

    # COUNT 参数需要放最后面
    4000000 =
    ```

### 运行 ###

1. 执行命令
    执行默认配置文件： user_config/default.conf

    ```shell
    python /your_location/monkey_android/performance/monkey/monkey_server.py`
    ```
    执行自定义配置文件(monkey_android/user_config 路径下)：user_config/custom.conf

    ```shell
    python /your_location/monkey_android/performance/monkey/monkey_server.py user_config/custom.conf
    ```
    或者使用配置文件的全路径
    ```shell
    python /your_location/monkey_android/performance/monkey/monkey_server.py /your_dir/custom.conf
    ```
2. 连接手机

### 关闭monkey ###

1. 停掉monkey_server或当前电脑没有正在运行的 monkey_server
2. 运行monkey_stop

    ```shell
    python /your_location/monkey_android/performance/monkey/monkey_stop.py
    ```
3. 或连接一台没有monkey_server 的电脑，执行重启手机

    ```shell
    adb reboot
    ```


### 邮件截图 ###
<img alt="summary" src="https://github.com/wangyunshuai/monkey_android/blob/master/performance/img/mail.png">



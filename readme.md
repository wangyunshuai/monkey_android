# Auto Monkey For Android

###功能简介
1. 完全自动：只需要负责连接设备
2. 支持多个设备
3. 支持随时断开设备、插入新设备，每5s定时检测设备自动运行
4. 崩溃后，发送邮件，邮件内容：执行时长、crash log

###系统及环境、依赖
1. 测试环境：Mac OS、Python 2.7.10
2. 配置 **adb**

###配置修改
/your_location/monkey_android/performance/config/config.py

```
class Config:
    # 配置 package_name, adb_location, mail_host, mail_user, mail_pass
    package_name = "com.testerhome.nativeandroid"
    adb_location = '/your_location/sdk/platform-tools/adb'
    mail_host = "smtp.163.com"  # 设置邮箱服务器
    mail_user = "xxxxx@163.com"  # 邮箱用户名
    mail_pass = "xxxxx"  # 邮箱密码
    mail_to_list = ['xxxxx@163.com'] # 发送给收件人
```

###运行
1. 执行命令 `python /your_location/monkey_android/performance/monkey/monkey_server.py`
2. 连接手机



###邮件截图
<img alt="summary" src="https://github.com/wangyunshuai/monkey_android/blob/master/performance/img/mail.png">

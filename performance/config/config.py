# /usr/bin/env python
# -*- encoding: utf-8 -*-

import os
import time
import logging
import platform
import random

project_name = "performance"
wkdir = os.getcwd()
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s %(levelname)s [line:%(lineno)d] %(message)s',
                    datefmt='%y%m%d %H:%M:%S',
                    filename='%s%s%s%slog%s%s.log' % (
                        wkdir, os.sep, project_name, os.sep, os.sep, time.strftime("%Y%m%d %H-%M-%S")),
                    filemode='w')
if True:
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s %(levelname)s | %(message)s    --[%(filename)-5s:%(lineno)d]')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)


class Config:

    # 配置 package_name, adb_location, mail_host, mail_user, mail_pass
    package_name = "com.testerhome.nativeandroid"
    adb_location = '/Users/smzdm/Documents/01_Android/adt-bundle-mac-x86_64-20140702/sdk/platform-tools/adb'
    mail_host = "smtp.163.com"  # 设置邮箱服务器
    mail_user = "yunswang@163.com"  # 邮箱用户名
    mail_pass = "wangjianhui"  # 邮箱密码
    mail_to_list = ['yunswang@163.com'] # 发送给收件人

    if platform.system() == 'Darwin':
        adb = adb_location
    elif platform.system() == 'Windows':
        adb = 'adb '
    device_dict = {}
    thread_instances = []
    thread_instances_monkey = []
    table_list = []
    taken_time = "1.5"
    mail_pre_title = "Automation-Monkey "
    result_table_name = "Result"
    str_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
    data_num = 1000
    monkey_seed = str(random.randrange(1, 1000))

    def __init__(self):
        pass


if __name__ == '__main__':

    pass

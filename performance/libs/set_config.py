#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import logging
import traceback
import ConfigParser

if __name__ == '__main__':
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config

reload(sys)
sys.setdefaultencoding('utf-8')


def set_custom_config(config_file):
    if os.path.exists(config_file) is True:
        config_parser = ConfigParser.ConfigParser()
        config_parser.read(config_file)
        Config.package_name = config_parser.get('config', 'package_name')
        Config.adb_location = config_parser.get('config', 'adb_location')
        Config.adb = config_parser.get('config', 'adb_location')
        Config.mail_host = config_parser.get('config', 'mail_host')
        Config.mail_user = config_parser.get('config', 'mail_user')
        Config.mail_pass = config_parser.get('config', 'mail_pass')
        Config.mail_to_list = config_parser.options('mail_to_list')

        monkey_parameters_list = config_parser.items('monkey_parameters')
        monkey_parameters = ""
        for i in monkey_parameters_list:
            monkey_parameters += "%s %s " % (i[0], i[1])
        Config.monkey_parameters = monkey_parameters

if __name__ == '__main__':
    config_file = "/Users/smzdm/Documents/git/monkey_android/default.conf"
    set_custom_config(config_file)



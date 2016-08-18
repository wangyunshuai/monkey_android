#! /usr/bin/python
# coding: utf-8

import os
import sys
import logging
import traceback

project_dir = os.path.split(sys.path[0])
project_dir = os.path.split(project_dir[0])
sys.path.append(project_dir[0])
os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)
wkdir = os.getcwd()

from performance.libs.set_config import set_custom_config

custom_config = sys.argv
if len(custom_config) == 1:
    logging.info("Use default config for monkey test")
    set_custom_config(os.path.join(wkdir, 'user_config/default.conf'))
elif len(custom_config) == 2:
    logging.info("Use custom config for monkey test")
    config_file = os.path.join(wkdir, custom_config[1])
    if os.path.exists(config_file) is True:
        set_custom_config(config_file)
    else:
        logging.info("Can not find .conf file, please re_check. conf file location input is: %s" % config_file)
        sys.exit()
else:
    logging.info("Only need one conf file, please check command line")

from performance.config.config import Config
from performance.libs.device_monitor import monitor_device

config = Config()


def run():
    logging.info('start server')
    monitor_device()

if __name__ == '__main__':
    try:
        pass
        run()
    except Exception:
        traceback.print_exc()
    finally:
        pass

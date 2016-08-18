#! /usr/bin/python
# coding: utf-8

import time
import os
import sys
import logging

if __name__ == '__main__':
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config
from performance.libs.base import get_device_info, start_adb
from performance.monkey.monkey import create_threads_monkey

def monitor_device():
    start_adb()
    while True:
        # logging.info("monitor_device")
        time.sleep(5)
        current_device_dict = {}
        new_device_dict = {}
        current_device_dict = get_device_info()
        logging.debug('current device dict: %s' % current_device_dict)
        logging.debug('Config.device_dict is %s' % Config.device_dict)
        if current_device_dict != Config.device_dict:
            for device_model, device_id in current_device_dict.iteritems():
                if device_model not in Config.device_dict:
                    new_device_dict.update({device_model: device_id})

            if new_device_dict != {}:
                logging.debug('new device dict is: %s' % new_device_dict)
            else:
                logging.info('device lost')
            Config.device_dict = current_device_dict
            create_threads_monkey(new_device_dict)
            # restart_threads()

if __name__ == '__main__':
    pass



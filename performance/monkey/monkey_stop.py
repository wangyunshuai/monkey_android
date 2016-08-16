#! /usr/bin/python
# coding: utf-8

import time
import commands
import re
import os
import sys
import platform
import subprocess
import logging

if __name__ == '__main__':
    project_dir = os.path.split(sys.path[0])
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config
from performance.libs.base import get_device_info
import performance.libs.base as base

adb = Config.adb


def stop_monkey(device_id, device_model):
    for i in xrange(10):
        output = ''
        if platform.system() == 'Darwin':
            status, output = commands.getstatusoutput(adb + ' -s %s shell ps | grep monkey' % device_id)
        elif platform.system() == 'Windows':
            try:
                output = subprocess.check_output('adb shell ps|findstr /e monkey', shell=True)
            except Exception as e:
                logging.error("stop monkey: %s" % e)

        if output == "error: device not found":
            logging.info("Please check device")
        elif output != "":
            logging.info('monkey info: %s' % output)
            output = re.search('shell     [0-9]+', output).group()
            pid = re.search('[0-9]+', output).group()
            logging.info("kill the monkey process: %s in %s" % (pid, device_model))
            if base.is_mac():
                status, output = commands.getstatusoutput("%s -s %s shell kill %s" % (adb, device_id, pid))
            elif base.is_win():
                subprocess.call(adb + ' shell kill ' + pid, shell=True)
        else:
            logging.info("no monkey running")
            break
    time.sleep(3)

if __name__ == '__main__':
    device_dict = get_device_info()
    for device_model, device_id in device_dict.iteritems():
        stop_monkey(device_id, device_model)

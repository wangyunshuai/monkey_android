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
    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)
    os.chdir(os.path.dirname(sys.argv[0]))      # 添加此文件所在路径为 working directory
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    wkdir = project_dir[0]
    sys.path.append(wkdir)
    os.chdir(wkdir)    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config
from performance.libs.base import get_device_info

adb = Config.adb


def stop_monkey(device_id, device_model):
    for i in xrange(10):
        if platform.system() == 'Darwin':
            status, output = commands.getstatusoutput(adb + ' -s %s shell ps | grep monkey' % device_id)
        elif platform.system() == 'Windows':
            output = subprocess.check_output(adb + " shell ps | findstr /e monkey", shell=True)

        if output == "error: device not found":
            logging.info("Please check device")
        elif output != "":
            output = re.search('shell     [0-9]+', output).group()
            pid = re.search('[0-9]+', output).group()
            logging.info("kill the monkey process: %s in %s" % (pid, device_model))
            # (status, output) = commands.getstatusoutput(adb + 'shell kill ' + pid)
            status, output = commands.getstatusoutput("%s -s %s shell kill %s" % (adb, device_id, pid))
        else:
            # logging.info("no monkey running")
            break
    time.sleep(3)

if __name__ == '__main__':
    device_dict = get_device_info()
    for device_model, device_id in device_dict.iteritems():
        stop_monkey(device_id, device_model)

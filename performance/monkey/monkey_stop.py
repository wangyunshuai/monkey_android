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
import traceback

if __name__ == '__main__':
    project_dir = os.path.split(sys.path[0])
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config
from performance.libs.base import get_device_info

adb = Config.adb

def stop_monkey_for_mac(device_id, device_model):
    for i in xrange(10):
        status, output = commands.getstatusoutput(adb + ' -s %s shell ps | grep monkey' % device_id)
        if output == "error: device not found":
            logging.debug("Please check device")
        elif output == "":
            logging.info("no monkey running in %s" % device_model)
            break
        else:
            output = re.search('shell     [0-9]+', output).group()
            pid = re.search('[0-9]+', output).group()
            logging.info("kill the monkey process: %s in %s" % (pid, device_model))
            status, output = commands.getstatusoutput("%s -s %s shell kill %s" % (adb, device_id, pid))
        time.sleep(2)

def stop_monkey_for_win(device_id, device_model):
    for i in xrange(10):
        output = None
        cmd_pid = "%s -s %s shell ps | grep monkey" % (adb, device_id)
        try:
            output = subprocess.check_output(cmd_pid)
        except Exception:
            traceback.print_exc()
        if output == '':
            logging.info("No monkey running in %s" % device_model)
            break
        else:
            output = re.search('shell     [0-9]+', output).group()
            pid = re.search('[0-9]+', output).group()
            logging.info("kill the monkey process: %s in %s" % (pid, device_model))
            output = subprocess.check_output("%s -s %s shell kill %s" % (adb, device_id, pid))
    time.sleep(2)

def stop_monkey(device_id, device_model):
    if platform.system() == 'Darwin':
        logging.debug('This system is Mac')
        stop_monkey_for_mac(device_id, device_model)
    elif platform.system() == 'Windows':
        logging.debug('This system is Windows')
        stop_monkey_for_win(device_id, device_model)
    else:
        logging.info('Do not surpport your system')

if __name__ == '__main__':
    device_dict = get_device_info()
    for device_model, device_id in device_dict.iteritems():
        stop_monkey(device_id, device_model)

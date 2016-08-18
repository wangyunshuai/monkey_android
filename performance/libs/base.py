#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os
import platform
import commands
import sys
import time
import logging
import subprocess
import traceback

if __name__ == '__main__':
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config

reload(sys)
sys.setdefaultencoding('utf-8')

config = Config()
adb = config.adb

def start_adb():
    if platform.system() == 'Windows':
        subprocess.check_output('adb devices', shell=True)
    else:
        commands.getstatusoutput('adb devices')
    time.sleep(2)

def get_info_from_mac():
    '''返回 device id 和 device model'''
    device_dict = {}
    get_device_id_cmd = "%s devices | grep '\tdevice'" % adb
    (status, output) = commands.getstatusoutput(get_device_id_cmd)
    # logging.info(output)
    if output == '':
        logging.info('All device lost')
    else:
        output = output.split("\n")
        # logging.info(output)
        device_id_list = []
        for device_id in output:
            device_id = device_id.replace("\tdevice", "")
            device_id_list.append(device_id)
        # logging.info(device_id_list)

        for device_id in device_id_list:
            device_model = ""
            get_device_model_cmd = "%s -s %s shell getprop ro.product.model" % (adb, device_id)
            # logging.info(get_device_model_cmd)
            (status, output) = commands.getstatusoutput(get_device_model_cmd)
            # logging.info("'%s'" %output)
            output = output.strip("\r") # 去除行尾的换行光标
            output = output.split(" ")
            for i in output:
                device_model += i
            # logging.info("'%s'" %device_model)
            device_dict.update({device_model: device_id})
        logging.debug("get the device info: %s" % device_dict)
    return device_dict

def get_info_from_win():
    '''返回 device model 和 device id'''
    device_dict = {}
    get_device_id_cmd = "%s devices | findstr /e device" % adb   # /e 对一行的结尾进行匹配
    try:
        output = subprocess.check_output(get_device_id_cmd, shell=True)
        logging.debug('connected devices:\r%s' % output)
    except Exception:
        # traceback.print_exc()
        logging.info("All device lost")
        output = None
    if output is not None:
        output = output.split("\n")
        logging.debug('split connect devices id: %s' % output)
        device_id_list = []
        for device_id in output:
            if 'device' in device_id:
                logging.debug('get device: %s' % device_id)
                device_id = device_id.replace("\tdevice\r", "")
                device_id_list.append(device_id)
        logging.debug('got devices id: %s' % device_id_list)

        for device_id in device_id_list:
            device_model = ""
            get_device_model_cmd = "%s -s %s shell getprop ro.product.model" % (adb, device_id)
            # logging.info(get_device_model_cmd)
            try:
                output_model = subprocess.check_output(get_device_model_cmd, shell=True)
                logging.debug("'%s'" % output_model)
            except Exception:
                logging.error('get device model error')
                traceback.print_exc()
                output_model = None
            if output_model is not None:
                output_model = output_model.strip("\r\r\n") # 去除行尾的换行光标
                logging.debug(output_model)
                output_model = output_model.split(' ')
            for i in output_model:
                device_model += i
            # logging.info("'%s'" %device_model)
            device_dict.update({device_model: device_id})
        logging.debug("get the device info: %s" % device_dict)
    return device_dict

def get_device_info():
    if platform.system() == "Darwin":
        return get_info_from_mac()
    elif platform.system() == "Windows":
        return get_info_from_win()

if __name__ == '__main__':
    get_device_info()
    pass


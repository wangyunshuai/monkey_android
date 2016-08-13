#! /usr/bin/env python
# -*- coding: utf-8 -*-

import os, platform, commands
import subprocess
import sys
import re
import logging

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

def is_mac():
    return platform.system() == 'Darwin'

def is_win():
    return platform.system() == 'Windows'

def get_device_info():
    '''返回 device id 和 device model'''
    device_dict = {}
    device_id_list = []
    if is_mac():
        get_device_id_cmd = "%s devices | grep '\tdevice'" % adb
        # logging.info(adb_cmd)
        (status, output) = commands.getstatusoutput(get_device_id_cmd)
        # logging.info(output)
        output = output.split("\n")
        # logging.info(output)
        
        for device_id in output:
            device_id = device_id.replace("\tdevice", "")
            device_id_list.append(device_id)
        # logging.info(device_id_list)
    elif is_win():
        os.system('adb devices > devices.txt')
        fp = open('devices.txt')
        lines = fp.readlines()
        dviceUdid = []
        fp.close()
        for el in lines[1:-1]:
            list = re.split('\\t',el)
            device_id_list.append(list[0])
            
    if len(device_id_list) == 0:
        logging.info('All device lost')
    else:
        
        for device_id in device_id_list:
            device_model = "Darwin"
            get_device_model_cmd = "%s -s %s shell getprop ro.product.model" % (adb, device_id)
            logging.info(get_device_model_cmd)
            if is_mac():
                (status, output) = commands.getstatusoutput(get_device_model_cmd)
            elif is_win():
                output = subprocess.check_output(get_device_model_cmd, shell=True)
            output = output.strip('\n')
            output = output.strip("\r") # 去除行尾的换行光标
            output = output.split(" ")
            logging.info("'%s'" %output)
            for i in output:
                device_model += i.strip('\n').strip('\r\r')
            logging.info("'%s'" %device_model)
            device_dict.update({device_model: device_id})
        logging.info(device_dict)
    return device_dict

if __name__ == '__main__':
    a = get_device_info()
    logging.info(a)
    pass





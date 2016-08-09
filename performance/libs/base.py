#! /usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import print_function
import os, platform, commands
import sys
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

def get_device_info():
    '''返回 device id 和 device model'''
    device_dict = {}
    if platform.system() == 'Darwin':
        get_device_id_cmd = "%s devices | grep '\tdevice'" % adb
        # logging.info(adb_cmd)
        (status, output) = commands.getstatusoutput(get_device_id_cmd)
        # logging.info(output)
    elif platform.system() == 'Windows':
        pass
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
        # logging.info(device_dict)
    return device_dict

if __name__ == '__main__':
    a = get_device_info()
    logging.info(a)
    pass





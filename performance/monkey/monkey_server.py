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

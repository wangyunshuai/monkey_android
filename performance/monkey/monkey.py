#! /usr/bin/python
# coding: utf-8

import time
import commands
import os
import sys
import logging
import threading
import platform
import subprocess
import traceback

if __name__ == '__main__':
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config
from performance.libs.mail import SendMail
from performance.monkey.monkey_stop import stop_monkey

wkdir = os.getcwd()
adb = Config.adb
package_name = Config.package_name
monkey_seed = Config.monkey_seed
monkey_parameters = Config.monkey_parameters


def main(device_id, device_model):
    try:
        stop_monkey(device_id, device_model)

        log_file_name = generate_log_file_name(device_model)
        log_file_name_with_location = generate_log_file_name_with_location(device_model)
        monkey_duration = start_monkey(adb, device_id, device_model, monkey_seed, monkey_parameters, package_name)
        capture_screen(device_id, log_file_name, log_file_name_with_location, monkey_duration)
        mail_content = deal_with_log(log_file_name_with_location, monkey_duration)
        mail = SendMail()
        if mail_content == '':
            mail_content = 'No crash happened'
        mail.send_mail(Config.mail_to_list, mail_content)
        reboot_device(device_id, device_model)
    except Exception:
        traceback.print_exc()


def get_apk_name():
    abspath = os.path.abspath(__file__)
    current_location = os.path.split(abspath)[0]
    files_in_current_location = os.listdir(current_location)

    for i in files_in_current_location:
        if 'apk' in i:
            apk_name = i
    return apk_name

# def reinstall():
#     # uninstall & install app
#     location_apk=os.path.join(current_location, apk_name)
#     print location_apk

#     print '\runinstalling...'
#     output = subprocess.check_output(adb + '-s ' + device_id + ' uninstall ' + package_name, shell=True)
#     print output
#     print '\rinstalling...'
#     output = subprocess.check_output(adb + '-s ' + device_id + ' install ' + location_apk, shell=True)
#     print output

#     print 'reboot device...'
#     output = subprocess.check_output(adb + '-s ' + device_id + ' reboot', shell=True)
#     count_time = 0
#     for i in range(60):
#       time.sleep(1)
#       count_time += 1
#       print count_time,
#     print


def generate_log_file_name(device_model):
    # 生成 crash log 名字
    current_time = time.strftime("%m-%d~%H-%M-%S")
    log_file_name = device_model + '_' + current_time
    return log_file_name


def generate_log_file_name_with_location(device_model):
    # 获取当前 Log 存储路径
    location_log = os.path.join(wkdir, 'performance', 'monkey', 'monkeylog')
    current_date = time.strftime("%Y-%m-%d")
    current_date = os.path.join(location_log, current_date)
    if os.path.exists(current_date) is False:
        os.mkdir(current_date)
    log_file_name = generate_log_file_name(device_model)
    log_file_name_with_location = os.path.join(current_date, log_file_name)
    return log_file_name_with_location


def start_monkey(adb, device_id, device_model, monkey_seed, monkey_parameters, package_name):
    logging.info("start monkey with %s" % device_model)
    log_file_name_with_location = generate_log_file_name_with_location(device_model)
    monkey_start_time = time.time()
    cmd_monkey = "%s -s %s shell monkey -s %s -p %s %s > %s.txt" % (
        adb, device_id, monkey_seed, package_name, monkey_parameters, log_file_name_with_location)
    # cmd_monkey = "%s -s %s shell monkey -s %s -p %s --pct-touch 10 --pct-motion 10 --pct-appswitch 80 -v 400000000 > %s.txt" %(adb, device_id, monkey_seed, package_name, log_file_name_with_location)
    if platform.system() == "Darwin":
        logging.info("Monkey cmd: %s" % cmd_monkey)
        status, output = commands.getstatusoutput(cmd_monkey)
    elif platform.system() == "Windows":
        logging.info("Monkey cmd: %s" % cmd_monkey)
        output = subprocess.check_output(cmd_monkey, shell=True)
    logging.info("monkey end with %s" % device_model)
    monkey_end_time = time.time()
    monkey_duration = round((monkey_end_time - monkey_start_time) / 3600, 2)
    return str(monkey_duration)


def capture_screen(device_id, log_file_name, log_file_name_with_location, monkey_duration):
    logging.info("capture screen")
    cmd_capture = "%s -s %s shell screencap -p /sdcard/%s.png" % (adb, device_id, log_file_name)
    status, output = commands.getstatusoutput(cmd_capture)
    if output == "":
        cmd_pull_screenshot = "%s -s %s pull /sdcard/%s.png %s.png" % (
            adb, device_id, log_file_name, log_file_name_with_location)
        status, output = commands.getstatusoutput(cmd_pull_screenshot)
        logging.info(output)
    # rename log file
    if output == "":
        log_file_name_location_final = log_file_name_with_location + '_' + monkey_duration
        os.rename(log_file_name_with_location + '.png', log_file_name_location_final + '.png')


def deal_with_log(log_file_name_with_location, monkey_duration):
    # analyze with log:
    logging.info("deal_with_log")
    f_full_log = open(log_file_name_with_location + '.txt', 'r')
    full_log = f_full_log.readlines()
    f_full_log.close()
    full_log_lines_number = len(full_log)
    anr = '// NOT RESPONDING: ' + package_name + ' '
    exception = '// CRASH: ' + package_name + ' '
    mail_content = ''
    for i in xrange(full_log_lines_number):
        if (exception in full_log[i]) | (anr in full_log[i]):
            f_crash_log = open(log_file_name_with_location + '.txt', 'r')
            f_crash_log.close()
            for j in range(i, full_log_lines_number):
                mail_content = mail_content + full_log[j] + '\r'
                # f_crash_log = open(log_file_name_with_location + '.txt', 'a+')
                # f_crash_log.writelines(full_log[j])
                # f_crash_log.close()
            break
    if mail_content == "":
        return mail_content
    else:
        # rename log file
        log_file_name_location_final = log_file_name_with_location + ' ' + monkey_duration + "hour"
        tmp = log_file_name_with_location.split('/')
        # logging.info(tmp)
        log_file_name = tmp[-1]
        mail_content = log_file_name + '_' + monkey_duration + "hour" + '\r\r' + mail_content
        os.rename(log_file_name_with_location + '.txt', log_file_name_location_final + '.txt')
        return mail_content


def reboot_device(device_id, device_model):
    if platform.system() == "Darwin":
        logging.info("Reboot %s" % device_model)
        status, output = commands.getstatusoutput(adb + ' -s ' + device_id + ' reboot')
    elif platform.system() == "Windows":
        subprocess.check_output("%s -s %s reboot" % (adb, device_id), shell=True)


class MonkeyThread(threading.Thread):
    def __init__(self, device_id, device_model):
        threading.Thread.__init__(self)
        self.thread_stop = False
        self.device_id = device_id
        self.device_model = device_model

    def run(self):
        time.sleep(6)
        main(self.device_id, self.device_model)

def create_threads_monkey(device_dict):
    thread_instances = []
    if device_dict != {}:
        logging.info('changed device: %s' % device_dict)
        for model_device, id_device in device_dict.iteritems():
            device_model = model_device
            device_id = id_device
            instance = MonkeyThread(device_id, device_model)
            thread_instances.append(instance)
        for instance in thread_instances:
            instance.start()

if __name__ == '__main__':
    pass


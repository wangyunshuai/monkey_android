#! /usr/bin/env python
# -*- coding: utf-8 -*-

from email.mime.text import MIMEText
import time
import smtplib
import logging
import traceback
import os
import sys

if __name__ == '__main__':
    project_dir = os.path.split(os.getcwd())
    project_dir = os.path.split(project_dir[0])
    sys.path.append(project_dir[0])
    os.chdir(project_dir[0])    # 将项目所在文件夹设置为 wkdir (目录下必须有 __init__.py 文件)

from performance.config.config import Config

config = Config()


class SendMail():
    '''
    send email
    '''

    def __init__(self):
        self.mail_host = config.mail_host  # 设置服务器
        self.mail_user = config.mail_user  # 用户名
        self.mail_pass = config.mail_pass  # 密码

        self.str_date = time.strftime('%Y-%m-%d  %H:%M', time.localtime(time.time()))

    def send_mail(self, to_list, content):
        me = " Automation" + "<" + self.mail_user + ">"
        msg = MIMEText(content, _subtype='plain', _charset='utf-8')
        msg['Subject'] = config.mail_pre_title + self.str_date
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            server = smtplib.SMTP()
            server.connect(self.mail_host)
            server.login(self.mail_user, self.mail_pass)
            server.sendmail(me, to_list, msg.as_string())
            server.close()
            logging.info("发送成功")
            return True
        except Exception:
            traceback.print_exc()
            logging.info("发送失败")
            return False

if __name__ == '__main__':

    # 测试邮箱是否配置成功
    mail = SendMail()
    mail.send_mail(config.mail_to_list, 'abcd')

#!/bin/env python
# -*- coding: utf-8 -*-
# @author DDDivano
# encoding=utf-8 vi:ts=4:sw=4:expandtab:ft=python


"""
notice 邮件提示
"""

import smtplib
import requests
from email.mime.text import MIMEText
from email.header import Header


def email_send(receiver, subject, content):
    """
    send
    """
    sender = "zhengtianyu@baidu.com"
    content = requests.get("http://paddletest.baidu-int.com:8081/#/paddle/integration/release%2F2.4")
    content.encoding = content.apparent_encoding
    content = content.text
    message = MIMEText(content, 'html', 'utf-8')
    message["To"] = Header(receiver)

    message['Subject'] = Header(subject, 'utf-8')

    try:
        smtpObj = smtplib.SMTP('mail2-in.baidu.com')
        smtpObj.sendmail(sender, receiver, message.as_string())
        print("邮件发送成功")
    except smtplib.SMTPException:
        print("邮件发送失败")


if __name__ == '__main__':
    email_send("zhengtianyu@baidu.com", "测试邮件服务", "<h1>H1标签</h1>")

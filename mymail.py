#!/usr/bin/env python
# -*- coding:utf-8 -*-
from smtplib import SMTP_SSL
from email.mime.text import MIMEText
from email.header import Header


def send_mail(html):
    mail_info = {
        "from": "taomercy@qq.com",
        "to": "taomercy@qq.com",
        "hostname": "smtp.qq.com",
        "username": "taomercy@qq.com",
        "password": "hxbrvuwjkfnbiehd",
        "mail_subject": "stock monitor",
        "mail_text": html,
        "mail_encoding": "utf-8"
    }
    smtp = SMTP_SSL(mail_info["hostname"])
    # smtp.set_debuglevel(1)

    smtp.ehlo(mail_info["hostname"])
    smtp.login(mail_info["username"], mail_info["password"])
    msg = MIMEText(mail_info["mail_text"], _subtype="html", _charset=mail_info["mail_encoding"])
    msg["Subject"] = Header(mail_info["mail_subject"], mail_info["mail_encoding"])
    msg["From"] = mail_info["from"]
    msg["To"] = ",".join(mail_info["to"])

    smtp.sendmail(mail_info["from"], mail_info["to"], msg.as_string())
    smtp.quit()

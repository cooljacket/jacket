# -*- coding: utf-8 -*-
import smtplib
import email.mime.multipart
import email.mime.text


EMAIL_HOST = 'zuoyela_jacket@sina.com'
EMAIL_PASS = 'caibudao233666'
SMTP_SERVER = 'smtp.sina.com'
SMTP_PORT = '25'

def send_email(to_list, sub, content):
	msg=email.mime.multipart.MIMEMultipart()
	msg['from'] = EMAIL_HOST
	msg['to'] = ";".join(to_list)
	msg['subject'] = sub
	txt = email.mime.text.MIMEText(content)
	msg.attach(txt)

	smtp=smtplib
	smtp=smtplib.SMTP()
	smtp.connect(SMTP_SERVER, SMTP_PORT)
	smtp.login(EMAIL_HOST, EMAIL_PASS)
	for to in to_list:
		print(smtp.sendmail(EMAIL_HOST, to, str(msg)))
	smtp.quit()

#send_email(['1101925754@qq.com', '18819461579@163.com', 'insysujacket@gmail.com'], '测试哈哈', '正在测试中...\n换行可否？')
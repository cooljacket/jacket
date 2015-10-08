# -*- coding: utf-8 -*-
import smtplib  
from email.mime.text import MIMEText  


mail_host="smtp.sina.com"       #设置服务器
mail_user="zuoyela_jacket"      #用户名
mail_pass="caibudao233666"           #口令 
mail_postfix="sina.com"         #发件箱的后缀

mail_sender="作业LA"            #在邮件里看到的发送者名称

def send_email(to_list, sub, content):  
    '''
    发送邮件
    参数：
        to_list ([string]) - 收件人列表
        sub     (string)   - 主题
        content (string)   - 邮件内容
    '''
    me = mail_sender + "<" + mail_user + "@" + mail_postfix + ">"   #这里的hello可以任意设置，收到信后，将按照设置显示
    msg = MIMEText(content,_subtype='html',_charset='gb2312')    #创建一个实例，这里设置为html格式邮件
    msg['Subject'] = sub    #设置主题
    msg['From'] = me
    msg['To'] = ";".join(to_list)  
    try:  
        s = smtplib.SMTP()  
        s.connect(mail_host)  #连接smtp服务器
        s.login(mail_user, mail_pass)  #登陆服务器
        s.sendmail(me, to_list, msg.as_string())  #发送邮件
        s.close()  
        return True  
    except:
        return False


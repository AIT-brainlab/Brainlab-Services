from __future__ import print_function
import json

import os

import base64

import smtplib
from email.mime.text import MIMEText
# If modifying these scopes, delete the file token.json.

email_account:dict[str,str]
with open('/run/secrets/email_app_password.json') as r:
    email_account = json.load(r)
def gmail(to:str,subject:str,message_txt:str):


    message = MIMEText(message_txt,'html')
    message['To'] = to
    message['From'] = email_account['email']
    message['Subject'] = subject

    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.login(email_account['email'],email_account['app_password'])
    server.sendmail(email_account['email'],to,message.as_string())
    server.quit()
   





if __name__ == "__main__":
    gmail("raknatee@gmail.com","demo storybowl","""
    demo Hi test 2
    """)
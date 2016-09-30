"""
Creating and sending emails from Gmail - finding all files by type in a directory
account - ibtestmail123@gmail.com
pas - testmailpass

Target directory - should be changed on row 29
Filetype - should be changed on row 30
Receiver mail - should be changed on row 25
"""

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.utils import formatdate
from email import encoders

import os

fromail = "ibtestmail123@gmail.com"  # account to send from
testpass = 'testmailpass'  # password for the account to send from
mailport = 587
destmail = "iskra.bratovanova@gmail.com"  # recipient mail (may be a list)
textinmail = "New downloaded books"  # message body
subj = "Here are the new books"  # message subject
attachmode = "rb"
outputdir = "D:\SoftUni\Python\myProjects\webdownloader\output"
filetype = ".doc"


def prepare_attached_files():
    newfiles = os.listdir(outputdir)  # get the contents of a dir
    newdocfiles = []
    for f in newfiles:
        if filetype in f:
            newdocfiles.append(f)
    filestoattach = newdocfiles  # files that will be attached
    return filestoattach


def create_attachments(filestoattach):
    msg = MIMEMultipart()
    msg['From'] = fromail
    msg['To'] = destmail
    # msg['Date'] = formatdate(localtime = True)
    msg['Subject'] = subj
    msg.attach(MIMEText(textinmail))

    for file in filestoattach:
        filepath = os.path.join(outputdir, file)
        part = MIMEBase('application', "octet-stream")
        part.set_payload(open(filepath, attachmode).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=file)
        msg.attach(part)
    return msg


def send_mail(msg):
    mymail = smtplib.SMTP('smtp.gmail.com', mailport)
    mymail.ehlo()  # must be included
    mymail.starttls()  # must be included
    mymail.login(fromail, testpass)
    mymail.sendmail(fromail, destmail, msg.as_string())
    mymail.quit()


attached_files = prepare_attached_files()
mail_to_send = create_attachments(attached_files)
send_mail(mail_to_send)

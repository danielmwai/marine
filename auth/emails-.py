"""Test email."""
# !/usr/bin/python
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from django.conf import settings


def send_email(email, tmsg, hmsg, setting=settings, params={}):
    """Method to send emails."""
    try:
        sender = settings.EMAIL_HOST_USER
        password = settings.EMAIL_HOST_PASSWORD
        host = settings.EMAIL_HOST
        port = settings.EMAIL_PORT
        fmail = "Marine Insurance <%s>" % (sender)
        subject = "Marine Insurance Email Validation"
        msg = MIMEMultipart('alternative')
        if 'subject' in params:
            subject = params['subject']
        msg['Subject'] = subject
        msg['From'] = fmail
        msg['To'] = email

        part1 = MIMEText(tmsg, 'plain')
        part2 = MIMEText(hmsg, 'html')

        msg.attach(part1)
        msg.attach(part2)

        s = smtplib.SMTP_SSL(host, port, timeout=5)
        s.starttls()
        s.login(sender, password)
        s.sendmail(sender, email, msg.as_string())
        s.quit()
    except Exception, e:
        print 'Error sending email - %s' % (str(e))
    else:
        pass
